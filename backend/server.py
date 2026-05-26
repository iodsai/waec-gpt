"""WAEC Math Platform - FastAPI backend (V2: multi-topic, exams, admin, similar, solver verify)."""

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, UploadFile, File, Form
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import base64
import random
import hashlib
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt as pyjwt

from emergentintegrations.llm.chat import LlmChat, UserMessage

from seed_data_v3 import (
    TOPICS_V3 as TOPICS_V2,
    SUBTOPICS_BY_TOPIC_V3 as SUBTOPICS_BY_TOPIC,
    LESSONS_V3 as LESSONS_V2,
    QUESTIONS_V3,
)
from seed_data_v3_extra import EXTRA_SUBTOPICS, EXTRA_LESSONS, EXTRA_QUESTIONS

# Activate the 5 previously coming-soon topics + merge their subtopics/lessons/questions
_EXTRA_TOPIC_IDS = set(EXTRA_SUBTOPICS.keys())
for _t in TOPICS_V2:
    if _t["id"] in _EXTRA_TOPIC_IDS:
        _t["status"] = "available"
SUBTOPICS_BY_TOPIC = {**SUBTOPICS_BY_TOPIC, **EXTRA_SUBTOPICS}
LESSONS_V2 = {**LESSONS_V2, **EXTRA_LESSONS}
QUESTIONS_V3 = QUESTIONS_V3 + EXTRA_QUESTIONS
from sympy_verify import verify as sympy_verify
from playground_solver import solve_general
from ai_helpers import extract_question_from_image, generate_similar_questions
from waec_scraper import WAEC_PAPERS, extract_paper

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']
JWT_SECRET = os.environ['JWT_SECRET']
EMERGENT_LLM_KEY = os.environ['EMERGENT_LLM_KEY']
JWT_ALGO = "HS256"
JWT_EXPIRY_DAYS = 7

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Combined catalog
ALL_SUBTOPICS = []
for tid, subs in SUBTOPICS_BY_TOPIC.items():
    for s in subs:
        ALL_SUBTOPICS.append({**s, "topic": tid})

SUBTOPIC_NAME = {s["id"]: s["name"] for s in ALL_SUBTOPICS}
SUBTOPIC_TOPIC = {s["id"]: s["topic"] for s in ALL_SUBTOPICS}
TOPIC_NAME = {t["id"]: t["name"] for t in TOPICS_V2}

# ============ MODELS ============
class RegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str
    name: str
    email: str
    is_admin: bool = False
    created_at: str

class AuthResp(BaseModel):
    token: str
    user: UserPublic

class LessonNote(BaseModel):
    heading: str
    body: str

class Lesson(BaseModel):
    subtopic_id: str
    topic: str
    title: str
    summary: str
    notes: List[LessonNote]

class Question(BaseModel):
    id: str
    topic: str
    topic_name: str
    subtopic: str
    subtopic_name: str
    year: int
    difficulty: str
    question: str
    options: List[str]
    question_type: str = "objective"

class QuestionDetail(Question):
    answer: str
    solution_steps: List[str]

class AttemptReq(BaseModel):
    question_id: str
    selected: str

class AttemptResp(BaseModel):
    correct: bool
    correct_answer: str
    solution_steps: List[str]

class ChatReq(BaseModel):
    session_id: str
    message: str

class ChatResp(BaseModel):
    reply: str
    session_id: str

class ExamStartReq(BaseModel):
    mode: Literal["quick", "mock"]
    topic: Optional[str] = None  # if None, mixed
    question_ids: Optional[List[str]] = None  # custom set (e.g. revision deck)

class ExamQuestion(BaseModel):
    id: str
    topic: str
    topic_name: str
    subtopic: str
    subtopic_name: str
    question: str
    options: List[str]

class ExamStartResp(BaseModel):
    exam_id: str
    mode: str
    topic: Optional[str]
    duration_seconds: int
    questions: List[ExamQuestion]
    started_at: str

class ExamSubmitReq(BaseModel):
    answers: dict  # question_id -> selected option

class ExamReport(BaseModel):
    exam_id: str
    mode: str
    topic: Optional[str]
    total_questions: int
    correct: int
    score_percent: float
    time_taken_seconds: int
    by_subtopic: dict
    detail: List[dict]
    started_at: str
    submitted_at: str

class SimilarReq(BaseModel):
    n: int = 3

class SolverVerifyReq(BaseModel):
    equation: str
    claimed_answer: Optional[str] = None
    variable: str = "x"

class PlaygroundReq(BaseModel):
    expression: str
    operation: Literal["auto", "solve", "differentiate", "integrate", "simplify", "factor", "expand", "evaluate"] = "auto"
    variable: str = "x"

class AdminCreateQuestionReq(BaseModel):
    topic: str
    subtopic: str
    year: int
    difficulty: Literal["easy", "medium", "hard"]
    question: str
    options: List[str]
    answer: str
    solution_steps: List[str]

class WaecImportReq(BaseModel):
    paper_url: str
    year: int
    max_questions: int = 13

class WaecBulkSaveReq(BaseModel):
    paper_url: str
    year: int
    questions: List[dict]  # each: subtopic, difficulty, question, options, answer, solution_steps

class BookmarkToggleReq(BaseModel):
    question_id: str

# ============ HELPERS ============
def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())

def make_token(user_id: str) -> str:
    payload = {"user_id": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRY_DAYS)}
    return pyjwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await db.users.find_one({"id": payload["user_id"]}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def require_admin(current=Depends(get_current_user)):
    if not current.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    return current

def topic_of(subtopic_id: str) -> str:
    return SUBTOPIC_TOPIC.get(subtopic_id, "statistics")

# ============ LIFESPAN: SEED ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Drop legacy General Maths content + waeconline imports (pivot to Further Maths V3)
    fm_topics = ["statistics", "calculus", "vectors", "sets-logic", "surds-polynomials",
                 "sequences-binomial", "matrices", "mechanics"]
    deleted = await db.questions.delete_many({"topic": {"$nin": fm_topics}})
    await db.questions.delete_many({"source_url": {"$regex": "/Mathematics/", "$options": "i"}})
    if deleted.deleted_count:
        logging.info(f"Dropped {deleted.deleted_count} legacy General Maths questions")

    # Seed Further Maths content if empty
    if await db.questions.count_documents({}) == 0:
        docs = [{
            "id": str(uuid.uuid4()),
            "topic": q["topic"], "subtopic": q["subtopic"],
            "year": q["year"], "difficulty": q["difficulty"],
            "question": q["question"], "options": q["options"],
            "answer": q["answer"], "solution_steps": q["solution_steps"],
            "question_type": "objective", "source": "seed",
            "created_at": datetime.now(timezone.utc).isoformat(),
        } for q in QUESTIONS_V3]
        if docs:
            await db.questions.insert_many(docs)
            logging.info(f"Seeded {len(docs)} Further Maths questions")

    # Top-up: seed any new topics that have no questions yet (idempotent per-topic)
    for _tid in _EXTRA_TOPIC_IDS:
        if await db.questions.count_documents({"topic": _tid, "source": "seed"}) == 0:
            topic_qs = [q for q in EXTRA_QUESTIONS if q["topic"] == _tid]
            if topic_qs:
                await db.questions.insert_many([{
                    "id": str(uuid.uuid4()),
                    "topic": q["topic"], "subtopic": q["subtopic"],
                    "year": q["year"], "difficulty": q["difficulty"],
                    "question": q["question"], "options": q["options"],
                    "answer": q["answer"], "solution_steps": q["solution_steps"],
                    "question_type": "objective", "source": "seed",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                } for q in topic_qs])
                logging.info(f"Top-up seeded {len(topic_qs)} questions for topic '{_tid}'")

    # Backfill question_type if missing
    await db.questions.update_many({"question_type": {"$exists": False}}, {"$set": {"question_type": "objective"}})

    # Seed demo student + admin
    if not await db.users.find_one({"email": "student@waec.com"}):
        await db.users.insert_one({
            "id": str(uuid.uuid4()), "name": "Demo Student", "email": "student@waec.com",
            "password_hash": hash_password("Student@123"), "is_admin": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    if not await db.users.find_one({"email": "admin@waec.com"}):
        await db.users.insert_one({
            "id": str(uuid.uuid4()), "name": "Admin", "email": "admin@waec.com",
            "password_hash": hash_password("Admin@123"), "is_admin": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    else:
        await db.users.update_one({"email": "admin@waec.com"}, {"$set": {"is_admin": True}})
    await db.users.update_many({"is_admin": {"$exists": False}}, {"$set": {"is_admin": False}})

    # Mark any orphaned 'running' import jobs as 'interrupted' (background tasks die on reload)
    await db.import_jobs.update_many(
        {"status": "running"},
        {"$set": {
            "status": "interrupted",
            "interrupted_at": datetime.now(timezone.utc).isoformat(),
        }}
    )

    yield
    client.close()


app = FastAPI(title="WAEC Elective Math AI", lifespan=lifespan)
api = APIRouter(prefix="/api")

# ============ AUTH ROUTES ============
def _user_to_public(u: dict) -> UserPublic:
    return UserPublic(id=u["id"], name=u["name"], email=u["email"],
                      is_admin=bool(u.get("is_admin", False)), created_at=u["created_at"])

@api.post("/auth/register", response_model=AuthResp)
async def register(req: RegisterReq):
    existing = await db.users.find_one({"email": req.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_doc = {
        "id": str(uuid.uuid4()), "name": req.name.strip(), "email": req.email.lower(),
        "password_hash": hash_password(req.password), "is_admin": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.users.insert_one(user_doc)
    return AuthResp(token=make_token(user_doc["id"]), user=_user_to_public(user_doc))

@api.post("/auth/login", response_model=AuthResp)
async def login(req: LoginReq):
    user = await db.users.find_one({"email": req.email.lower()})
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResp(token=make_token(user["id"]), user=_user_to_public(user))

@api.get("/auth/me", response_model=UserPublic)
async def me(current=Depends(get_current_user)):
    return _user_to_public(current)

# ============ CATALOG ROUTES ============
@api.get("/topics")
async def get_topics():
    """Returns all topics with their subtopics."""
    enriched = []
    for t in TOPICS_V2:
        subs = SUBTOPICS_BY_TOPIC.get(t["id"], [])
        count = await db.questions.count_documents({"topic": t["id"]}) if t["status"] == "available" else 0
        enriched.append({**t, "subtopics": subs, "question_count": count})
    return {"topics": enriched}

@api.get("/lessons/{subtopic_id}", response_model=Lesson)
async def get_lesson(subtopic_id: str):
    lesson = LESSONS_V2.get(subtopic_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return Lesson(
        subtopic_id=subtopic_id,
        topic=topic_of(subtopic_id),
        title=lesson["title"], summary=lesson["summary"],
        notes=[LessonNote(**n) for n in lesson["notes"]],
    )

def _qpublic(d: dict) -> Question:
    return Question(
        id=d["id"],
        topic=d.get("topic", topic_of(d["subtopic"])),
        topic_name=TOPIC_NAME.get(d.get("topic", topic_of(d["subtopic"])), ""),
        subtopic=d["subtopic"],
        subtopic_name=SUBTOPIC_NAME.get(d["subtopic"], d["subtopic"]),
        year=d["year"], difficulty=d["difficulty"],
        question=d["question"], options=d.get("options", []),
        question_type=d.get("question_type", "objective"),
    )

@api.get("/questions", response_model=List[Question])
async def list_questions(
    topic: Optional[str] = None,
    subtopic: Optional[str] = None,
    year: Optional[int] = None,
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None,
    limit: int = 500,
):
    q: dict = {}
    if topic: q["topic"] = topic
    if subtopic: q["subtopic"] = subtopic
    if year: q["year"] = year
    if difficulty: q["difficulty"] = difficulty
    docs = await db.questions.find(q, {"_id": 0, "answer": 0, "solution_steps": 0}).to_list(limit)
    return [_qpublic(d) for d in docs]

@api.get("/questions/{qid}", response_model=QuestionDetail)
async def get_question(qid: str):
    d = await db.questions.find_one({"id": qid}, {"_id": 0})
    if not d: raise HTTPException(status_code=404, detail="Question not found")
    tname = TOPIC_NAME.get(d.get("topic", topic_of(d["subtopic"])), "")
    return QuestionDetail(
        id=d["id"], topic=d.get("topic", topic_of(d["subtopic"])), topic_name=tname,
        subtopic=d["subtopic"], subtopic_name=SUBTOPIC_NAME.get(d["subtopic"], d["subtopic"]),
        year=d["year"], difficulty=d["difficulty"],
        question=d["question"], options=d.get("options", []),
        question_type=d.get("question_type", "objective"),
        answer=d["answer"], solution_steps=d["solution_steps"],
    )

@api.get("/years")
async def list_years(topic: Optional[str] = None):
    q = {"topic": topic} if topic else {}
    years = await db.questions.distinct("year", q)
    return sorted(years, reverse=True)

# ============ ATTEMPTS / PROGRESS ============
@api.post("/attempts", response_model=AttemptResp)
async def submit_attempt(req: AttemptReq, current=Depends(get_current_user)):
    qdoc = await db.questions.find_one({"id": req.question_id}, {"_id": 0})
    if not qdoc:
        raise HTTPException(status_code=404, detail="Question not found")
    is_theory = qdoc.get("question_type") == "theory"
    correct = (not is_theory) and req.selected.strip() == qdoc["answer"].strip()
    await db.attempts.insert_one({
        "id": str(uuid.uuid4()), "user_id": current["id"], "question_id": req.question_id,
        "topic": qdoc.get("topic", topic_of(qdoc["subtopic"])),
        "subtopic": qdoc["subtopic"], "selected": req.selected, "correct": correct,
        "is_reveal": is_theory,  # theory reveals don't count toward accuracy
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return AttemptResp(correct=correct, correct_answer=qdoc["answer"], solution_steps=qdoc["solution_steps"])

@api.get("/progress")
async def get_progress(current=Depends(get_current_user)):
    # Exclude theory "reveal" entries from accuracy stats
    attempts = await db.attempts.find(
        {"user_id": current["id"], "$or": [{"is_reveal": {"$exists": False}}, {"is_reveal": False}]},
        {"_id": 0}
    ).to_list(5000)
    total = len(attempts)
    correct = sum(1 for a in attempts if a["correct"])
    acc = round((correct / total) * 100, 1) if total else 0.0
    by_sub: dict = {}
    by_topic: dict = {}
    for a in attempts:
        s = a["subtopic"]
        if s not in by_sub:
            by_sub[s] = {"total": 0, "correct": 0, "name": SUBTOPIC_NAME.get(s, s)}
        by_sub[s]["total"] += 1
        if a["correct"]: by_sub[s]["correct"] += 1
        t = a.get("topic", topic_of(s))
        if t not in by_topic:
            by_topic[t] = {"total": 0, "correct": 0, "name": TOPIC_NAME.get(t, t)}
        by_topic[t]["total"] += 1
        if a["correct"]: by_topic[t]["correct"] += 1
    for v in by_sub.values():
        v["accuracy"] = round((v["correct"] / v["total"]) * 100, 1)
    for v in by_topic.values():
        v["accuracy"] = round((v["correct"] / v["total"]) * 100, 1)
    recent = sorted(attempts, key=lambda x: x["created_at"], reverse=True)[:10]
    qids = [r["question_id"] for r in recent]
    qmap: dict = {}
    if qids:
        async for qd in db.questions.find({"id": {"$in": qids}}, {"_id": 0, "id": 1, "question": 1}):
            qmap[qd["id"]] = qd["question"]
    for r in recent:
        r["question_text"] = qmap.get(r["question_id"], "")
        r["subtopic_name"] = SUBTOPIC_NAME.get(r["subtopic"], r["subtopic"])
    return {
        "total_attempts": total, "correct": correct, "accuracy": acc,
        "by_subtopic": by_sub, "by_topic": by_topic, "recent_attempts": recent,
    }

@api.get("/progress/weak-spot")
async def weak_spot(current=Depends(get_current_user)):
    """Return the student's lowest-accuracy subtopic with ≥3 attempts.
    If they have fewer attempts, suggest a fresh topic with question_count > 0.
    """
    attempts = await db.attempts.find(
        {"user_id": current["id"], "$or": [{"is_reveal": {"$exists": False}}, {"is_reveal": False}]},
        {"_id": 0}
    ).to_list(5000)

    MIN_ATTEMPTS = 3
    by_sub: dict = {}
    for a in attempts:
        s = a["subtopic"]
        by_sub.setdefault(s, {"total": 0, "correct": 0})
        by_sub[s]["total"] += 1
        if a["correct"]:
            by_sub[s]["correct"] += 1

    eligible = [
        {"subtopic": s, "topic": SUBTOPIC_TOPIC.get(s),
         "subtopic_name": SUBTOPIC_NAME.get(s, s),
         "topic_name": TOPIC_NAME.get(SUBTOPIC_TOPIC.get(s, ""), ""),
         "total": v["total"], "correct": v["correct"],
         "accuracy": round((v["correct"] / v["total"]) * 100, 1)}
        for s, v in by_sub.items() if v["total"] >= MIN_ATTEMPTS
    ]

    if eligible:
        eligible.sort(key=lambda x: x["accuracy"])
        weakest = eligible[0]
        return {
            "kind": "weak_spot",
            "subtopic": weakest["subtopic"],
            "subtopic_name": weakest["subtopic_name"],
            "topic": weakest["topic"],
            "topic_name": weakest["topic_name"],
            "accuracy": weakest["accuracy"],
            "total_attempts": weakest["total"],
            "message": f"You score {weakest['accuracy']}% on {weakest['subtopic_name']} — let's strengthen it.",
        }

    # Fallback: suggest an unexplored topic
    attempted_subs = set(by_sub.keys())
    untouched = [s for s in ALL_SUBTOPICS if s["id"] not in attempted_subs]
    if untouched:
        pick = untouched[0]
        return {
            "kind": "explore",
            "subtopic": pick["id"],
            "subtopic_name": pick["name"],
            "topic": pick["topic"],
            "topic_name": TOPIC_NAME.get(pick["topic"], ""),
            "accuracy": None,
            "total_attempts": 0,
            "message": f"Try {pick['name']} — fresh ground to start exploring.",
        }

    return {"kind": "none", "message": "Practise a few questions and we'll spot your weak areas."}


def _card(kind: str, sub: dict, label: str, message: str, accuracy=None, total_attempts=0):
    return {
        "kind": kind,
        "label": label,
        "subtopic": sub["id"] if "id" in sub else sub["subtopic"],
        "subtopic_name": sub.get("name") or sub.get("subtopic_name"),
        "topic": sub.get("topic") or SUBTOPIC_TOPIC.get(sub.get("subtopic", "")),
        "topic_name": TOPIC_NAME.get(sub.get("topic") or SUBTOPIC_TOPIC.get(sub.get("subtopic", ""), ""), ""),
        "accuracy": accuracy,
        "total_attempts": total_attempts,
        "message": message,
    }


@api.get("/progress/daily-plan")
async def daily_plan(current=Depends(get_current_user)):
    """Return a 3-card daily study plan: weak, medium, new (or 'explore' / 'none' fallbacks)."""
    attempts = await db.attempts.find(
        {"user_id": current["id"], "$or": [{"is_reveal": {"$exists": False}}, {"is_reveal": False}]},
        {"_id": 0}
    ).to_list(5000)

    MIN_ATTEMPTS = 3
    by_sub: dict = {}
    for a in attempts:
        s = a["subtopic"]
        by_sub.setdefault(s, {"total": 0, "correct": 0})
        by_sub[s]["total"] += 1
        if a["correct"]:
            by_sub[s]["correct"] += 1

    eligible = sorted([
        {"subtopic": s, "topic": SUBTOPIC_TOPIC.get(s),
         "subtopic_name": SUBTOPIC_NAME.get(s, s),
         "total": v["total"], "correct": v["correct"],
         "accuracy": round((v["correct"] / v["total"]) * 100, 1)}
        for s, v in by_sub.items() if v["total"] >= MIN_ATTEMPTS
    ], key=lambda x: x["accuracy"])

    used_subs: set = set()
    cards: list = []

    # 1) WEAK — lowest accuracy
    if eligible:
        w = eligible[0]
        used_subs.add(w["subtopic"])
        cards.append(_card(
            "weak", w, "Strengthen",
            f"You score {w['accuracy']}% on {w['subtopic_name']} — close the gap.",
            accuracy=w["accuracy"], total_attempts=w["total"],
        ))

    # 2) MEDIUM — middle-of-the-pack accuracy (60–80%) or median if not enough range
    medium_pool = [x for x in eligible if x["subtopic"] not in used_subs and 50 <= x["accuracy"] < 85]
    if not medium_pool:
        medium_pool = [x for x in eligible if x["subtopic"] not in used_subs]
    if medium_pool:
        m = medium_pool[len(medium_pool) // 2]
        used_subs.add(m["subtopic"])
        cards.append(_card(
            "medium", m, "Push harder",
            f"You're at {m['accuracy']}% on {m['subtopic_name']} — push toward mastery.",
            accuracy=m["accuracy"], total_attempts=m["total"],
        ))

    # 3) NEW — an unexplored subtopic from a topic the student hasn't touched (or any)
    attempted_subs = set(by_sub.keys()) | used_subs
    untouched = [s for s in ALL_SUBTOPICS if s["id"] not in attempted_subs]
    if untouched:
        # Prefer a subtopic from a topic with the fewest attempts
        topic_attempts: dict = {}
        for s, v in by_sub.items():
            t = SUBTOPIC_TOPIC.get(s, "")
            topic_attempts[t] = topic_attempts.get(t, 0) + v["total"]
        untouched.sort(key=lambda s: topic_attempts.get(s["topic"], 0))
        n = untouched[0]
        cards.append(_card(
            "new", n, "Explore",
            f"Try {n['name']} — fresh ground to expand your range.",
            accuracy=None, total_attempts=0,
        ))

    if not cards:
        return {"cards": [], "message": "Practise a few questions and we'll build your daily plan."}

    return {"cards": cards, "message": None}

# ============ BOOKMARKS ============
@api.get("/predictions")
async def topic_predictions(current=Depends(get_current_user)):
    """Predict top-5 likely subtopics for the next WAEC paper based on past-paper frequency.
    Only counts questions from real scraped papers (not seed data)."""
    # Count subtopic appearances across imported papers
    pipeline = [
        {"$match": {"source": {"$in": ["waeconline", "waeconline-batch"]}}},
        {"$group": {"_id": "$subtopic", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 8},
    ]
    rows = await db.questions.aggregate(pipeline).to_list(20)
    total = sum(r["count"] for r in rows) or 1
    items = []
    for r in rows[:5]:
        sub = r["_id"]
        items.append({
            "subtopic": sub,
            "subtopic_name": SUBTOPIC_NAME.get(sub, sub),
            "topic": SUBTOPIC_TOPIC.get(sub, ""),
            "topic_name": TOPIC_NAME.get(SUBTOPIC_TOPIC.get(sub, ""), ""),
            "appearances": r["count"],
            "frequency_pct": round((r["count"] / total) * 100, 1),
        })
    paper_count = await db.questions.count_documents(
        {"source": {"$in": ["waeconline", "waeconline-batch"]}}
    )
    return {
        "items": items,
        "sample_size": paper_count,
        "papers_analysed": 29,
    }


@api.get("/question-of-the-day")
async def question_of_the_day(current=Depends(get_current_user)):
    """Return one deterministic question for today (UTC date). Same for everyone, changes at midnight UTC."""
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Hash the date to pick a stable question index
    seed = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    # Only objective questions of medium/hard difficulty for daily challenge
    pool = await db.questions.find(
        {"$and": [
            {"$or": [{"question_type": {"$exists": False}}, {"question_type": "objective"}]},
            {"difficulty": {"$in": ["medium", "hard"]}},
        ]},
        {"_id": 0, "answer": 0, "solution_steps": 0},
    ).to_list(2000)
    if not pool:
        return {"question": None, "date": today_str}
    pool.sort(key=lambda q: q["id"])  # stable order
    pick = pool[seed % len(pool)]
    # Check whether the user already attempted today's question
    attempt = await db.attempts.find_one(
        {"user_id": current["id"], "question_id": pick["id"],
         "$expr": {"$gte": ["$created_at", today_str]}},
        {"_id": 0},
    )
    return {
        "date": today_str,
        "question": {
            "id": pick["id"],
            "question": pick["question"],
            "options": pick["options"],
            "subtopic": pick["subtopic"],
            "subtopic_name": SUBTOPIC_NAME.get(pick["subtopic"], pick["subtopic"]),
            "topic": pick.get("topic", topic_of(pick["subtopic"])),
            "topic_name": TOPIC_NAME.get(pick.get("topic", topic_of(pick["subtopic"])), ""),
            "year": pick["year"],
            "difficulty": pick["difficulty"],
        },
        "already_attempted": bool(attempt),
        "attempt_correct": attempt.get("correct") if attempt else None,
    }


@api.post("/bookmarks/toggle")
async def toggle_bookmark(req: BookmarkToggleReq, current=Depends(get_current_user)):
    """Toggle bookmark for a question. Returns the new state."""
    existing = await db.bookmarks.find_one(
        {"user_id": current["id"], "question_id": req.question_id}, {"_id": 0}
    )
    if existing:
        await db.bookmarks.delete_one({"user_id": current["id"], "question_id": req.question_id})
        return {"bookmarked": False}
    # Verify question exists
    q = await db.questions.find_one({"id": req.question_id}, {"_id": 0, "id": 1})
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    await db.bookmarks.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current["id"],
        "question_id": req.question_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return {"bookmarked": True}

@api.get("/bookmarks")
async def list_bookmarks(current=Depends(get_current_user)):
    """Return the student's revision deck — bookmarked questions with metadata."""
    marks = await db.bookmarks.find(
        {"user_id": current["id"]}, {"_id": 0}
    ).sort("created_at", -1).to_list(500)
    if not marks:
        return {"items": [], "count": 0}
    qids = [m["question_id"] for m in marks]
    docs = await db.questions.find(
        {"id": {"$in": qids}}, {"_id": 0, "answer": 0, "solution_steps": 0}
    ).to_list(500)
    by_id = {d["id"]: d for d in docs}
    items = []
    for m in marks:
        d = by_id.get(m["question_id"])
        if not d:
            continue
        items.append({
            "question_id": d["id"],
            "question": d["question"],
            "subtopic_name": SUBTOPIC_NAME.get(d["subtopic"], d["subtopic"]),
            "topic_name": TOPIC_NAME.get(d.get("topic", topic_of(d["subtopic"])), ""),
            "year": d["year"],
            "difficulty": d["difficulty"],
            "question_type": d.get("question_type", "objective"),
            "bookmarked_at": m["created_at"],
        })
    return {"items": items, "count": len(items)}

@api.get("/bookmarks/ids")
async def list_bookmark_ids(current=Depends(get_current_user)):
    """Compact list of bookmarked question_ids for client-side bookmark indicators."""
    marks = await db.bookmarks.find(
        {"user_id": current["id"]}, {"_id": 0, "question_id": 1}
    ).to_list(500)
    return {"ids": [m["question_id"] for m in marks]}

# ============ AI TUTOR ============
TUTOR_SYSTEM = """You are an expert WAEC Mathematics tutor for West African secondary school students (SS1-SS3).

Your role:
- Explain math concepts and solve problems clearly, in the style of a patient, encouraging WAEC examiner.
- Always show step-by-step working. Number each step (Step 1, Step 2, ...).
- Use LaTeX wrapped in single dollar signs for inline math like $x^2 + 3x$ and double dollar signs for display math like $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$.
- Specialise in: algebra, trigonometry, geometry, statistics, calculus, vectors.
- Mention common student mistakes when relevant.
- Keep tone warm, encouraging, and use simple English. End with a brief "Practice tip" when appropriate.
- If the question is non-mathematical, gently redirect to math topics.
"""

@api.post("/tutor/chat", response_model=ChatResp)
async def tutor_chat(req: ChatReq, current=Depends(get_current_user)):
    session_id = f"{current['id']}::{req.session_id}"
    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()), "user_id": current["id"], "session_id": req.session_id,
        "role": "user", "content": req.message,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    try:
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=session_id, system_message=TUTOR_SYSTEM)\
            .with_model("gemini", "gemini-3-flash-preview")
        reply = await chat.send_message(UserMessage(text=req.message))
    except Exception as e:
        logging.exception("AI tutor error")
        raise HTTPException(status_code=500, detail="AI tutor temporarily unavailable") from e

    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()), "user_id": current["id"], "session_id": req.session_id,
        "role": "assistant", "content": reply,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return ChatResp(reply=reply, session_id=req.session_id)

@api.get("/tutor/history/{session_id}")
async def tutor_history(session_id: str, current=Depends(get_current_user)):
    msgs = await db.chat_messages.find(
        {"user_id": current["id"], "session_id": session_id},
        {"_id": 0}
    ).sort("created_at", 1).to_list(500)
    return msgs

# ============ SOLVER (SymPy) ============
@api.post("/solver/verify")
async def solver_verify(req: SolverVerifyReq, current=Depends(get_current_user)):
    return sympy_verify(req.equation, req.claimed_answer, req.variable)

@api.post("/playground/solve")
async def playground_solve(req: PlaygroundReq, current=Depends(get_current_user)):
    """General-purpose SymPy solver — solve, differentiate, integrate, simplify, factor, expand, evaluate."""
    return solve_general(req.expression, req.operation, req.variable)

# ============ SIMILAR QUESTIONS ============
@api.post("/questions/{qid}/similar")
async def similar_questions(qid: str, req: SimilarReq, current=Depends(get_current_user)):
    q = await db.questions.find_one({"id": qid}, {"_id": 0})
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    src = {
        "id": q["id"], "question": q["question"], "options": q.get("options", []),
        "answer": q["answer"],
        "subtopic_name": SUBTOPIC_NAME.get(q["subtopic"], q["subtopic"]),
        "difficulty": q["difficulty"],
    }
    n = max(1, min(req.n, 5))
    try:
        items = await generate_similar_questions(EMERGENT_LLM_KEY, src, n=n)
    except Exception as e:
        logging.exception("similar generation failed")
        raise HTTPException(status_code=500, detail="Could not generate similar questions") from e
    return {"items": items, "count": len(items)}

# ============ EXAM MODE ============
EXAM_CONFIG = {
    "quick": {"count": 10, "duration_seconds": 5 * 60},
    "mock":  {"count": 40, "duration_seconds": 60 * 60},
}

@api.post("/exams/start", response_model=ExamStartResp)
async def exam_start(req: ExamStartReq, current=Depends(get_current_user)):
    cfg = EXAM_CONFIG[req.mode]
    objective_filter = {"$or": [{"question_type": {"$exists": False}}, {"question_type": "objective"}]}

    if req.question_ids:
        # Custom question set (e.g. revision deck). Honor provided IDs, filter to objective.
        q = {"id": {"$in": req.question_ids}, **objective_filter}
        docs = await db.questions.find(q, {"_id": 0}).to_list(2000)
        if not docs:
            raise HTTPException(status_code=400, detail="No objective questions found in this set")
        # Preserve caller-provided order, drop unknown ids
        by_id = {d["id"]: d for d in docs}
        sampled = [by_id[qid] for qid in req.question_ids if qid in by_id]
        # Duration scales with set size, using quick-mode pace (~30s/question), min 3 min
        duration = max(180, len(sampled) * 30)
    else:
        q: dict = dict(objective_filter)
        if req.topic and req.topic != "mixed":
            q["topic"] = req.topic
        docs = await db.questions.find(q, {"_id": 0}).to_list(2000)
        if len(docs) < 1:
            raise HTTPException(status_code=400, detail="Not enough questions for an exam in this scope")
        count = min(cfg["count"], len(docs))
        sampled = random.sample(docs, count)
        duration = cfg["duration_seconds"]

    started = datetime.now(timezone.utc)
    exam = {
        "id": str(uuid.uuid4()), "user_id": current["id"], "mode": req.mode, "topic": req.topic,
        "duration_seconds": duration,
        "question_ids": [d["id"] for d in sampled],
        "answers_map": {d["id"]: d["answer"] for d in sampled},
        "started_at": started.isoformat(),
        "submitted_at": None, "score": None,
        "source": "deck" if req.question_ids else "random",
    }
    await db.exams.insert_one(exam)
    return ExamStartResp(
        exam_id=exam["id"], mode=req.mode, topic=req.topic,
        duration_seconds=duration,
        questions=[
            ExamQuestion(
                id=d["id"],
                topic=d.get("topic", topic_of(d["subtopic"])),
                topic_name=TOPIC_NAME.get(d.get("topic", topic_of(d["subtopic"])), ""),
                subtopic=d["subtopic"],
                subtopic_name=SUBTOPIC_NAME.get(d["subtopic"], d["subtopic"]),
                question=d["question"], options=d["options"],
            ) for d in sampled
        ],
        started_at=started.isoformat(),
    )

@api.post("/exams/{exam_id}/submit", response_model=ExamReport)
async def exam_submit(exam_id: str, req: ExamSubmitReq, current=Depends(get_current_user)):
    exam = await db.exams.find_one({"id": exam_id, "user_id": current["id"]}, {"_id": 0})
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    if exam.get("submitted_at"):
        raise HTTPException(status_code=400, detail="Exam already submitted")

    # Fetch questions
    docs = await db.questions.find({"id": {"$in": exam["question_ids"]}}, {"_id": 0}).to_list(1000)
    by_id = {d["id"]: d for d in docs}
    detail = []
    by_sub: dict = {}
    correct_count = 0
    for qid in exam["question_ids"]:
        d = by_id.get(qid)
        if not d: continue
        sel = (req.answers.get(qid) or "").strip()
        is_correct = sel == d["answer"].strip()
        if is_correct: correct_count += 1
        s = d["subtopic"]
        by_sub.setdefault(s, {"name": SUBTOPIC_NAME.get(s, s), "total": 0, "correct": 0})
        by_sub[s]["total"] += 1
        if is_correct: by_sub[s]["correct"] += 1
        detail.append({
            "question_id": qid, "question": d["question"], "options": d["options"],
            "selected": sel, "correct_answer": d["answer"], "correct": is_correct,
            "subtopic_name": SUBTOPIC_NAME.get(s, s),
            "solution_steps": d["solution_steps"],
        })
        # also record as an attempt so dashboard reflects exam practice
        await db.attempts.insert_one({
            "id": str(uuid.uuid4()), "user_id": current["id"], "question_id": qid,
            "topic": d.get("topic", topic_of(s)), "subtopic": s,
            "selected": sel, "correct": is_correct, "from_exam": exam_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

    for v in by_sub.values():
        v["accuracy"] = round((v["correct"] / v["total"]) * 100, 1) if v["total"] else 0
    total_q = len(exam["question_ids"])
    score = round((correct_count / total_q) * 100, 1) if total_q else 0
    submitted = datetime.now(timezone.utc)
    started = datetime.fromisoformat(exam["started_at"])
    time_taken = int((submitted - started).total_seconds())

    await db.exams.update_one(
        {"id": exam_id},
        {"$set": {
            "submitted_at": submitted.isoformat(),
            "score": score, "correct": correct_count,
            "answers": req.answers, "time_taken_seconds": time_taken,
        }}
    )
    return ExamReport(
        exam_id=exam_id, mode=exam["mode"], topic=exam.get("topic"),
        total_questions=total_q, correct=correct_count, score_percent=score,
        time_taken_seconds=time_taken,
        by_subtopic=by_sub, detail=detail,
        started_at=exam["started_at"], submitted_at=submitted.isoformat(),
    )

@api.get("/exams/{exam_id}", response_model=ExamReport)
async def exam_report(exam_id: str, current=Depends(get_current_user)):
    exam = await db.exams.find_one({"id": exam_id, "user_id": current["id"]}, {"_id": 0})
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    if not exam.get("submitted_at"):
        raise HTTPException(status_code=400, detail="Exam not yet submitted")

    # rebuild detail from stored answers
    docs = await db.questions.find({"id": {"$in": exam["question_ids"]}}, {"_id": 0}).to_list(1000)
    by_id = {d["id"]: d for d in docs}
    detail = []
    by_sub: dict = {}
    for qid in exam["question_ids"]:
        d = by_id.get(qid)
        if not d: continue
        sel = (exam.get("answers", {}).get(qid) or "").strip()
        is_correct = sel == d["answer"].strip()
        s = d["subtopic"]
        by_sub.setdefault(s, {"name": SUBTOPIC_NAME.get(s, s), "total": 0, "correct": 0})
        by_sub[s]["total"] += 1
        if is_correct: by_sub[s]["correct"] += 1
        detail.append({
            "question_id": qid, "question": d["question"], "options": d["options"],
            "selected": sel, "correct_answer": d["answer"], "correct": is_correct,
            "subtopic_name": SUBTOPIC_NAME.get(s, s),
            "solution_steps": d["solution_steps"],
        })
    for v in by_sub.values():
        v["accuracy"] = round((v["correct"] / v["total"]) * 100, 1) if v["total"] else 0
    return ExamReport(
        exam_id=exam_id, mode=exam["mode"], topic=exam.get("topic"),
        total_questions=len(exam["question_ids"]),
        correct=exam.get("correct", 0), score_percent=exam.get("score", 0),
        time_taken_seconds=exam.get("time_taken_seconds", 0),
        by_subtopic=by_sub, detail=detail,
        started_at=exam["started_at"], submitted_at=exam["submitted_at"],
    )

@api.get("/exams")
async def list_exams(current=Depends(get_current_user)):
    docs = await db.exams.find(
        {"user_id": current["id"], "submitted_at": {"$ne": None}},
        {"_id": 0, "id": 1, "mode": 1, "topic": 1, "score": 1, "submitted_at": 1,
         "correct": 1, "question_ids": 1, "time_taken_seconds": 1}
    ).sort("submitted_at", -1).to_list(50)
    for d in docs:
        d["total_questions"] = len(d.pop("question_ids", []))
    return docs

# ============ ADMIN ============
@api.post("/admin/questions")
async def admin_create_question(req: AdminCreateQuestionReq, current=Depends(require_admin)):
    if req.subtopic not in SUBTOPIC_NAME:
        raise HTTPException(status_code=400, detail="Unknown subtopic")
    doc = {
        "id": str(uuid.uuid4()),
        "topic": req.topic, "subtopic": req.subtopic,
        "year": req.year, "difficulty": req.difficulty,
        "question": req.question, "options": req.options,
        "answer": req.answer, "solution_steps": req.solution_steps,
        "source": "admin", "created_by": current["id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.questions.insert_one(doc)
    return {"id": doc["id"], "ok": True}

@api.post("/admin/questions/extract")
async def admin_extract_question(image: UploadFile = File(...), current=Depends(require_admin)):
    contents = await image.read()
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 8MB)")
    b64 = base64.b64encode(contents).decode()
    mime = image.content_type or "image/jpeg"
    try:
        data = await extract_question_from_image(EMERGENT_LLM_KEY, b64, mime)
    except Exception as e:
        logging.exception("image extract failed")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}") from e
    return data

@api.get("/admin/questions")
async def admin_list_questions(current=Depends(require_admin)):
    docs = await db.questions.find({}, {"_id": 0}).sort("created_at", -1).to_list(500)
    return docs

@api.delete("/admin/questions/{qid}")
async def admin_delete_question(qid: str, current=Depends(require_admin)):
    r = await db.questions.delete_one({"id": qid})
    if r.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}

# ============ WAEC PAST PAPER IMPORT (admin) ============
@api.get("/admin/import/papers")
async def list_waec_papers(current=Depends(require_admin)):
    """Return the catalog of available WAEC papers."""
    return {"papers": WAEC_PAPERS}

@api.post("/admin/import/extract")
async def import_waec_paper(req: WaecImportReq, current=Depends(require_admin)):
    """Scrape + convert a WAEC paper to MCQ JSON (does NOT save).

    Latency: ~30-90 seconds per paper (13 Gemini Vision calls).
    """
    try:
        result = await extract_paper(EMERGENT_LLM_KEY, req.paper_url, req.year, max_questions=req.max_questions)
    except Exception as e:
        logging.exception("WAEC import failed")
        raise HTTPException(status_code=500, detail=f"Import failed: {e}") from e
    return result

@api.post("/admin/import/save")
async def save_imported_questions(req: WaecBulkSaveReq, current=Depends(require_admin)):
    """Persist accepted questions from a paper-import preview.

    Supports both `objective` (with options) and `theory` (no options) question types.
    """
    docs = []
    DEFAULT_SUB = "measures-of-location"
    for q in req.questions:
        subtopic = q.get("subtopic") or q.get("subtopic_guess") or DEFAULT_SUB
        if subtopic not in SUBTOPIC_NAME:
            subtopic = DEFAULT_SUB
        topic = SUBTOPIC_TOPIC.get(subtopic, "statistics")
        qtype = q.get("question_type") or ("theory" if not q.get("options") else "objective")
        doc = {
            "id": str(uuid.uuid4()),
            "topic": topic, "subtopic": subtopic,
            "year": req.year,
            "difficulty": q.get("difficulty") or q.get("difficulty_guess") or "medium",
            "question": q.get("question", "").strip(),
            "options": q.get("options", []) if qtype == "objective" else [],
            "answer": q.get("answer", ""),
            "solution_steps": q.get("solution_steps", []),
            "question_type": qtype,
            "source": "waeconline",
            "source_url": q.get("source_url") or req.paper_url,
            "created_by": current["id"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        if not doc["question"] or not doc["answer"]:
            continue
        # objective requires at least 2 options; theory does not
        if qtype == "objective" and len(doc["options"]) < 2:
            continue
        docs.append(doc)
    if not docs:
        raise HTTPException(status_code=400, detail="No valid questions in payload")
    await db.questions.insert_many(docs)
    return {"saved": len(docs), "ids": [d["id"] for d in docs]}

# ============ BATCH IMPORT (background) ============
import asyncio as _asyncio

FURTHER_MATHS_SUBTOPICS = {
    "measures-of-location", "measures-of-spread", "correlation", "probability",
    "perms-combinations", "limits", "differentiation", "applications-differentiation",
    "integration", "applications-integration", "vector-algebra-2d", "vectors-3d",
    "magnitude-direction", "scalar-product", "vectors-applications",
}

class BatchImportReq(BaseModel):
    year_from: int = 2010
    year_to: int = 2018
    max_questions_per_paper: int = 13


async def _run_batch_import(job_id: str, papers: list[dict], max_q: int):
    """Background worker — extracts each paper sequentially and saves accepted questions."""
    total_saved = 0
    total_extracted = 0
    errors: list[str] = []

    for idx, paper in enumerate(papers):
        try:
            await db.import_jobs.update_one(
                {"id": job_id},
                {"$set": {
                    "current_paper": paper["label"],
                    "current_year": paper["year"],
                    "progress_index": idx,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }}
            )
            result = await extract_paper(
                EMERGENT_LLM_KEY, paper["url"], paper["year"],
                max_questions=max_q,
            )
            qs = result.get("questions", [])
            total_extracted += len(qs)

            # Save inline (mirroring /admin/import/save logic but no auth checks)
            docs = []
            for q in qs:
                subtopic = q.get("subtopic") or q.get("subtopic_guess") or "measures-of-location"
                if subtopic not in FURTHER_MATHS_SUBTOPICS:
                    subtopic = "measures-of-location"
                qtype = q.get("question_type") or ("theory" if not q.get("options") else "objective")
                doc = {
                    "id": str(uuid.uuid4()),
                    "topic": SUBTOPIC_TOPIC.get(subtopic, "statistics"),
                    "subtopic": subtopic,
                    "year": paper["year"],
                    "difficulty": q.get("difficulty") or q.get("difficulty_guess") or "medium",
                    "question": (q.get("question") or "").strip(),
                    "options": q.get("options", []) if qtype == "objective" else [],
                    "answer": q.get("answer", ""),
                    "solution_steps": q.get("solution_steps", []),
                    "question_type": qtype,
                    "source": "waeconline-batch",
                    "source_url": q.get("source_url") or paper["url"],
                    "batch_job_id": job_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
                if not doc["question"] or not doc["answer"]:
                    continue
                if qtype == "objective" and len(doc["options"]) < 2:
                    continue
                docs.append(doc)
            if docs:
                await db.questions.insert_many(docs)
                total_saved += len(docs)

            await db.import_jobs.update_one(
                {"id": job_id},
                {"$set": {
                    "total_extracted": total_extracted,
                    "total_saved": total_saved,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
                 "$push": {"papers_done": {
                    "label": paper["label"], "year": paper["year"], "url": paper["url"],
                    "extracted": len(qs), "saved": len(docs),
                 }}}
            )
        except Exception as e:
            logging.exception("Batch paper failed: %s", paper.get("url"))
            errors.append(f"{paper['label']}: {str(e)[:200]}")
            await db.import_jobs.update_one(
                {"id": job_id},
                {"$push": {"errors": f"{paper['label']}: {str(e)[:200]}"}}
            )

    await db.import_jobs.update_one(
        {"id": job_id},
        {"$set": {
            "status": "completed",
            "total_saved": total_saved,
            "total_extracted": total_extracted,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }}
    )


@api.post("/admin/import/batch")
async def start_batch_import(req: BatchImportReq, current=Depends(require_admin)):
    """Start a background batch import for a range of years."""
    papers = [p for p in WAEC_PAPERS if req.year_from <= p["year"] <= req.year_to]
    if not papers:
        raise HTTPException(status_code=400, detail="No papers in that year range")

    # Prevent overlapping jobs
    running = await db.import_jobs.find_one({"status": "running"}, {"_id": 0})
    if running:
        raise HTTPException(status_code=409, detail=f"Batch job already running: {running['id']}")

    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "status": "running",
        "year_from": req.year_from,
        "year_to": req.year_to,
        "total_papers": len(papers),
        "progress_index": 0,
        "papers_done": [],
        "errors": [],
        "total_saved": 0,
        "total_extracted": 0,
        "started_by": current["id"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.import_jobs.insert_one(job)
    _asyncio.create_task(_run_batch_import(job_id, papers, req.max_questions_per_paper))
    return {"job_id": job_id, "total_papers": len(papers), "papers": [
        {"label": p["label"], "year": p["year"]} for p in papers
    ]}


@api.get("/admin/import/batch")
async def list_batch_jobs(current=Depends(require_admin)):
    jobs = await db.import_jobs.find({}, {"_id": 0}).sort("started_at", -1).to_list(20)
    return {"jobs": jobs}


@api.get("/admin/import/batch/{job_id}")
async def get_batch_job(job_id: str, current=Depends(require_admin)):
    job = await db.import_jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# ============ HEALTH ============
@api.get("/")
async def root():
    return {"status": "ok", "service": "WAEC Math AI", "version": "2.0"}

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
