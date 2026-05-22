"""WAEC Math Platform - FastAPI backend.

Routes:
- /api/auth/register, /api/auth/login, /api/auth/me
- /api/topics, /api/lessons/{subtopic_id}
- /api/questions (filters: subtopic, year, difficulty), /api/questions/{id}
- /api/attempts (POST submit), /api/progress (GET stats)
- /api/tutor/chat (Gemini 3 Flash via emergentintegrations)
"""

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt as pyjwt

from emergentintegrations.llm.chat import LlmChat, UserMessage

from seed_data import SUBTOPICS, LESSONS, QUESTIONS

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Env
MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']
JWT_SECRET = os.environ['JWT_SECRET']
EMERGENT_LLM_KEY = os.environ['EMERGENT_LLM_KEY']
JWT_ALGO = "HS256"
JWT_EXPIRY_DAYS = 7

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI(title="WAEC Math AI")
api = APIRouter(prefix="/api")

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
    created_at: str

class AuthResp(BaseModel):
    token: str
    user: UserPublic

class Subtopic(BaseModel):
    id: str
    name: str

class LessonNote(BaseModel):
    heading: str
    body: str

class Lesson(BaseModel):
    subtopic_id: str
    title: str
    summary: str
    notes: List[LessonNote]

class Question(BaseModel):
    id: str
    subtopic: str
    subtopic_name: str
    year: int
    difficulty: str
    question: str
    options: List[str]

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

class ProgressStats(BaseModel):
    total_attempts: int
    correct: int
    accuracy: float
    by_subtopic: dict
    recent_attempts: List[dict]

class ChatReq(BaseModel):
    session_id: str
    message: str

class ChatResp(BaseModel):
    reply: str
    session_id: str

# ============ HELPERS ============
def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())

def make_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRY_DAYS),
    }
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

def subtopic_name(sid: str) -> str:
    for s in SUBTOPICS:
        if s["id"] == sid:
            return s["name"]
    return sid

# ============ STARTUP: SEED ============
@app.on_event("startup")
async def startup_seed():
    # Seed questions
    count = await db.questions.count_documents({})
    if count == 0:
        docs = []
        for q in QUESTIONS:
            docs.append({
                "id": str(uuid.uuid4()),
                "subtopic": q["subtopic"],
                "year": q["year"],
                "difficulty": q["difficulty"],
                "question": q["question"],
                "options": q["options"],
                "answer": q["answer"],
                "solution_steps": q["solution_steps"],
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        await db.questions.insert_many(docs)
        logging.info(f"Seeded {len(docs)} questions")

    # Seed demo user
    demo_email = "student@waec.com"
    existing = await db.users.find_one({"email": demo_email})
    if not existing:
        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            "name": "Demo Student",
            "email": demo_email,
            "password_hash": hash_password("Student@123"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logging.info("Seeded demo user student@waec.com / Student@123")

# ============ AUTH ROUTES ============
@api.post("/auth/register", response_model=AuthResp)
async def register(req: RegisterReq):
    existing = await db.users.find_one({"email": req.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_doc = {
        "id": str(uuid.uuid4()),
        "name": req.name.strip(),
        "email": req.email.lower(),
        "password_hash": hash_password(req.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.users.insert_one(user_doc)
    return AuthResp(
        token=make_token(user_doc["id"]),
        user=UserPublic(id=user_doc["id"], name=user_doc["name"], email=user_doc["email"], created_at=user_doc["created_at"]),
    )

@api.post("/auth/login", response_model=AuthResp)
async def login(req: LoginReq):
    user = await db.users.find_one({"email": req.email.lower()})
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResp(
        token=make_token(user["id"]),
        user=UserPublic(id=user["id"], name=user["name"], email=user["email"], created_at=user["created_at"]),
    )

@api.get("/auth/me", response_model=UserPublic)
async def me(current=Depends(get_current_user)):
    return UserPublic(id=current["id"], name=current["name"], email=current["email"], created_at=current["created_at"])

# ============ CONTENT ROUTES ============
@api.get("/topics")
async def get_topics():
    # WAEC main topic for V1 is "Algebra" with subtopics
    return {
        "topic": "Algebra",
        "description": "Algebra for the WAEC SSCE syllabus.",
        "subtopics": SUBTOPICS,
    }

@api.get("/lessons/{subtopic_id}", response_model=Lesson)
async def get_lesson(subtopic_id: str):
    lesson = LESSONS.get(subtopic_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return Lesson(
        subtopic_id=subtopic_id,
        title=lesson["title"],
        summary=lesson["summary"],
        notes=[LessonNote(**n) for n in lesson["notes"]],
    )

@api.get("/questions", response_model=List[Question])
async def list_questions(
    subtopic: Optional[str] = None,
    year: Optional[int] = None,
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None,
):
    query: dict = {}
    if subtopic: query["subtopic"] = subtopic
    if year: query["year"] = year
    if difficulty: query["difficulty"] = difficulty
    docs = await db.questions.find(query, {"_id": 0, "answer": 0, "solution_steps": 0}).to_list(500)
    return [
        Question(
            id=d["id"], subtopic=d["subtopic"], subtopic_name=subtopic_name(d["subtopic"]),
            year=d["year"], difficulty=d["difficulty"], question=d["question"], options=d["options"],
        ) for d in docs
    ]

@api.get("/questions/{qid}", response_model=QuestionDetail)
async def get_question(qid: str):
    d = await db.questions.find_one({"id": qid}, {"_id": 0})
    if not d:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionDetail(
        id=d["id"], subtopic=d["subtopic"], subtopic_name=subtopic_name(d["subtopic"]),
        year=d["year"], difficulty=d["difficulty"], question=d["question"], options=d["options"],
        answer=d["answer"], solution_steps=d["solution_steps"],
    )

@api.get("/years")
async def list_years():
    years = await db.questions.distinct("year")
    return sorted(years, reverse=True)

# ============ ATTEMPTS / PROGRESS ============
@api.post("/attempts", response_model=AttemptResp)
async def submit_attempt(req: AttemptReq, current=Depends(get_current_user)):
    q = await db.questions.find_one({"id": req.question_id}, {"_id": 0})
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    correct = req.selected.strip() == q["answer"].strip()
    attempt = {
        "id": str(uuid.uuid4()),
        "user_id": current["id"],
        "question_id": req.question_id,
        "subtopic": q["subtopic"],
        "selected": req.selected,
        "correct": correct,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.attempts.insert_one(attempt)
    return AttemptResp(correct=correct, correct_answer=q["answer"], solution_steps=q["solution_steps"])

@api.get("/progress", response_model=ProgressStats)
async def get_progress(current=Depends(get_current_user)):
    attempts = await db.attempts.find({"user_id": current["id"]}, {"_id": 0}).to_list(2000)
    total = len(attempts)
    correct = sum(1 for a in attempts if a["correct"])
    acc = round((correct / total) * 100, 1) if total else 0.0
    by_sub: dict = {}
    for a in attempts:
        s = a["subtopic"]
        if s not in by_sub:
            by_sub[s] = {"total": 0, "correct": 0, "name": subtopic_name(s)}
        by_sub[s]["total"] += 1
        if a["correct"]:
            by_sub[s]["correct"] += 1
    for s, v in by_sub.items():
        v["accuracy"] = round((v["correct"] / v["total"]) * 100, 1)
    # most recent first
    recent = sorted(attempts, key=lambda x: x["created_at"], reverse=True)[:10]
    # attach question text for recent
    qids = [r["question_id"] for r in recent]
    qmap = {}
    if qids:
        async for qd in db.questions.find({"id": {"$in": qids}}, {"_id": 0, "id": 1, "question": 1}):
            qmap[qd["id"]] = qd["question"]
    for r in recent:
        r["question_text"] = qmap.get(r["question_id"], "")
        r["subtopic_name"] = subtopic_name(r["subtopic"])
    return ProgressStats(total_attempts=total, correct=correct, accuracy=acc, by_subtopic=by_sub, recent_attempts=recent)

# ============ AI TUTOR ============
TUTOR_SYSTEM = """You are an expert WAEC Mathematics tutor for West African secondary school students (SS1-SS3).

Your role:
- Explain math concepts and solve problems clearly, in the style of a patient, encouraging WAEC examiner.
- Always show step-by-step working. Number each step (Step 1, Step 2, ...).
- Use LaTeX wrapped in single dollar signs for inline math like $x^2 + 3x$ and double dollar signs for display math like $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$.
- Specialise in: linear equations, quadratics, simultaneous equations, indices, logarithms, variation, sequences/series, inequalities.
- Mention common student mistakes when relevant.
- Keep tone warm, encouraging, and use simple English. End with a brief "Practice tip" when appropriate.
- If the question is non-mathematical, gently redirect to math topics.
"""

@api.post("/tutor/chat", response_model=ChatResp)
async def tutor_chat(req: ChatReq, current=Depends(get_current_user)):
    session_id = f"{current['id']}::{req.session_id}"

    # Save user message
    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current["id"],
        "session_id": req.session_id,
        "role": "user",
        "content": req.message,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=TUTOR_SYSTEM,
        ).with_model("gemini", "gemini-3-flash-preview")

        reply = await chat.send_message(UserMessage(text=req.message))
    except Exception as e:
        logging.exception("AI tutor error")
        raise HTTPException(status_code=500, detail=f"AI tutor unavailable: {str(e)}")

    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current["id"],
        "session_id": req.session_id,
        "role": "assistant",
        "content": reply,
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

# ============ HEALTH ============
@api.get("/")
async def root():
    return {"status": "ok", "service": "WAEC Math AI"}

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
