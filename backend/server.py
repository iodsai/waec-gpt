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
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt as pyjwt

from emergentintegrations.llm.chat import LlmChat, UserMessage

from seed_data import LESSONS as ALGEBRA_LESSONS, QUESTIONS as ALGEBRA_QUESTIONS
from seed_data_v2 import (
    TOPICS_V2, SUBTOPICS_BY_TOPIC, LESSONS_V2,
    QUESTIONS_V2, ALGEBRA_EXTRA_QUESTIONS,
)
from sympy_verify import verify as sympy_verify
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
    return SUBTOPIC_TOPIC.get(subtopic_id, "algebra")

# ============ LIFESPAN: SEED ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed legacy algebra questions (with topic field)
    if await db.questions.count_documents({}) == 0:
        docs = []
        for q in ALGEBRA_QUESTIONS:
            docs.append({
                "id": str(uuid.uuid4()),
                "topic": "algebra",
                "subtopic": q["subtopic"],
                "year": q["year"], "difficulty": q["difficulty"],
                "question": q["question"], "options": q["options"],
                "answer": q["answer"], "solution_steps": q["solution_steps"],
                "source": "seed",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        # Trig + Geometry
        for q in QUESTIONS_V2:
            docs.append({
                "id": str(uuid.uuid4()),
                "topic": q["topic"], "subtopic": q["subtopic"],
                "year": q["year"], "difficulty": q["difficulty"],
                "question": q["question"], "options": q["options"],
                "answer": q["answer"], "solution_steps": q["solution_steps"],
                "source": "seed",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        # Extra algebra spanning 2010-2024
        for q in ALGEBRA_EXTRA_QUESTIONS:
            docs.append({
                "id": str(uuid.uuid4()),
                "topic": q["topic"], "subtopic": q["subtopic"],
                "year": q["year"], "difficulty": q["difficulty"],
                "question": q["question"], "options": q["options"],
                "answer": q["answer"], "solution_steps": q["solution_steps"],
                "source": "seed",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        await db.questions.insert_many(docs)
        logging.info(f"Seeded {len(docs)} questions")
    else:
        # Migration: backfill `topic` on existing docs missing it
        result = await db.questions.update_many(
            {"topic": {"$exists": False}},
            [{"$set": {"topic": {"$ifNull": [None, "algebra"]}}}]
        )
        if result.modified_count == 0:
            # try the simple set
            await db.questions.update_many({"topic": {"$exists": False}}, {"$set": {"topic": "algebra"}})

        # Add Trig/Geometry/extra-algebra questions if not yet present
        existing_total = await db.questions.count_documents({"source": "seed"})
        expected = len(ALGEBRA_QUESTIONS) + len(QUESTIONS_V2) + len(ALGEBRA_EXTRA_QUESTIONS)
        if existing_total < expected:
            # add only the new sets (V2 + algebra extra) if their topics/years missing
            new_docs = []
            for q in QUESTIONS_V2:
                exists = await db.questions.find_one({
                    "topic": q["topic"], "subtopic": q["subtopic"],
                    "year": q["year"], "question": q["question"],
                })
                if not exists:
                    new_docs.append({
                        "id": str(uuid.uuid4()), "topic": q["topic"], "subtopic": q["subtopic"],
                        "year": q["year"], "difficulty": q["difficulty"],
                        "question": q["question"], "options": q["options"],
                        "answer": q["answer"], "solution_steps": q["solution_steps"],
                        "source": "seed",
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    })
            for q in ALGEBRA_EXTRA_QUESTIONS:
                exists = await db.questions.find_one({
                    "topic": q["topic"], "subtopic": q["subtopic"],
                    "year": q["year"], "question": q["question"],
                })
                if not exists:
                    new_docs.append({
                        "id": str(uuid.uuid4()), "topic": q["topic"], "subtopic": q["subtopic"],
                        "year": q["year"], "difficulty": q["difficulty"],
                        "question": q["question"], "options": q["options"],
                        "answer": q["answer"], "solution_steps": q["solution_steps"],
                        "source": "seed",
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    })
            if new_docs:
                await db.questions.insert_many(new_docs)
                logging.info(f"Seeded {len(new_docs)} additional questions")

    # Seed demo student
    if not await db.users.find_one({"email": "student@waec.com"}):
        await db.users.insert_one({
            "id": str(uuid.uuid4()), "name": "Demo Student", "email": "student@waec.com",
            "password_hash": hash_password("Student@123"), "is_admin": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logging.info("Seeded demo user student@waec.com / Student@123")

    # Seed admin
    if not await db.users.find_one({"email": "admin@waec.com"}):
        await db.users.insert_one({
            "id": str(uuid.uuid4()), "name": "Admin", "email": "admin@waec.com",
            "password_hash": hash_password("Admin@123"), "is_admin": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logging.info("Seeded admin admin@waec.com / Admin@123")
    else:
        # Ensure existing admin user has is_admin flag
        await db.users.update_one({"email": "admin@waec.com"}, {"$set": {"is_admin": True}})

    # Backfill is_admin: false for any user missing the flag
    await db.users.update_many({"is_admin": {"$exists": False}}, {"$set": {"is_admin": False}})

    yield
    client.close()


app = FastAPI(title="WAEC Math AI V2", lifespan=lifespan)
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
    lesson = ALGEBRA_LESSONS.get(subtopic_id) or LESSONS_V2.get(subtopic_id)
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
    correct = req.selected.strip() == qdoc["answer"].strip()
    await db.attempts.insert_one({
        "id": str(uuid.uuid4()), "user_id": current["id"], "question_id": req.question_id,
        "topic": qdoc.get("topic", topic_of(qdoc["subtopic"])),
        "subtopic": qdoc["subtopic"], "selected": req.selected, "correct": correct,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return AttemptResp(correct=correct, correct_answer=qdoc["answer"], solution_steps=qdoc["solution_steps"])

@api.get("/progress")
async def get_progress(current=Depends(get_current_user)):
    attempts = await db.attempts.find({"user_id": current["id"]}, {"_id": 0}).to_list(5000)
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
    q: dict = {"$or": [{"question_type": {"$exists": False}}, {"question_type": "objective"}]}
    if req.topic and req.topic != "mixed":
        q["topic"] = req.topic
    docs = await db.questions.find(q, {"_id": 0}).to_list(2000)
    if len(docs) < 1:
        raise HTTPException(status_code=400, detail="Not enough questions for an exam in this scope")
    count = min(cfg["count"], len(docs))
    sampled = random.sample(docs, count)
    started = datetime.now(timezone.utc)
    exam = {
        "id": str(uuid.uuid4()), "user_id": current["id"], "mode": req.mode, "topic": req.topic,
        "duration_seconds": cfg["duration_seconds"],
        "question_ids": [d["id"] for d in sampled],
        "answers_map": {d["id"]: d["answer"] for d in sampled},
        "started_at": started.isoformat(),
        "submitted_at": None, "score": None,
    }
    await db.exams.insert_one(exam)
    return ExamStartResp(
        exam_id=exam["id"], mode=req.mode, topic=req.topic,
        duration_seconds=cfg["duration_seconds"],
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
    for q in req.questions:
        subtopic = q.get("subtopic") or q.get("subtopic_guess") or "linear-equations"
        if subtopic not in SUBTOPIC_NAME:
            subtopic = "linear-equations"
        topic = SUBTOPIC_TOPIC.get(subtopic, "algebra")
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
