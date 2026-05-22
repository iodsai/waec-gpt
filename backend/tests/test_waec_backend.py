"""Backend tests for WAEC Math AI platform.

Covers: auth (register/login/me), topics, lessons, questions, attempts,
progress, tutor (Gemini 3 Flash), years endpoint.
"""
import os
import uuid
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://mathmastery-waec.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

DEMO_EMAIL = "student@waec.com"
DEMO_PASS = "Student@123"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def demo_token(session):
    r = session.post(f"{API}/auth/login", json={"email": DEMO_EMAIL, "password": DEMO_PASS})
    assert r.status_code == 200, f"Demo login failed: {r.status_code} {r.text}"
    return r.json()["token"]


@pytest.fixture(scope="session")
def auth_headers(demo_token):
    return {"Authorization": f"Bearer {demo_token}", "Content-Type": "application/json"}


# ----- Health -----
def test_root(session):
    r = session.get(f"{API}/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


# ----- Auth -----
class TestAuth:
    def test_register_new_user(self, session):
        email = f"TEST_{uuid.uuid4().hex[:8]}@example.com"
        r = session.post(f"{API}/auth/register", json={
            "name": "Test User", "email": email, "password": "Pass@123"
        })
        assert r.status_code == 200, r.text
        data = r.json()
        assert "token" in data and isinstance(data["token"], str)
        assert data["user"]["email"] == email.lower()
        assert "id" in data["user"]

    def test_register_duplicate(self, session):
        r = session.post(f"{API}/auth/register", json={
            "name": "Demo", "email": DEMO_EMAIL, "password": "anything"
        })
        assert r.status_code == 400

    def test_login_demo(self, session):
        r = session.post(f"{API}/auth/login", json={"email": DEMO_EMAIL, "password": DEMO_PASS})
        assert r.status_code == 200
        d = r.json()
        assert d["user"]["email"] == DEMO_EMAIL
        assert len(d["token"]) > 20

    def test_login_invalid(self, session):
        r = session.post(f"{API}/auth/login", json={"email": DEMO_EMAIL, "password": "wrong"})
        assert r.status_code == 401

    def test_me_with_token(self, session, auth_headers):
        r = session.get(f"{API}/auth/me", headers=auth_headers)
        assert r.status_code == 200
        assert r.json()["email"] == DEMO_EMAIL

    def test_me_without_token(self, session):
        r = session.get(f"{API}/auth/me")
        assert r.status_code == 401


# ----- Content -----
class TestContent:
    def test_topics(self, session):
        r = session.get(f"{API}/topics")
        assert r.status_code == 200
        d = r.json()
        # V2: nested topics list
        assert "topics" in d
        algebra = next((t for t in d["topics"] if t["id"] == "algebra"), None)
        assert algebra is not None
        assert algebra["name"] == "Algebra"
        ids = {s["id"] for s in algebra["subtopics"]}
        assert "linear-equations" in ids and "quadratic-equations" in ids

    def test_lesson_linear(self, session):
        r = session.get(f"{API}/lessons/linear-equations")
        assert r.status_code == 200
        d = r.json()
        assert d["subtopic_id"] == "linear-equations"
        assert len(d["notes"]) >= 2

    def test_lesson_quadratic(self, session):
        r = session.get(f"{API}/lessons/quadratic-equations")
        assert r.status_code == 200
        assert r.json()["title"] == "Quadratic Equations"

    def test_lesson_not_found(self, session):
        r = session.get(f"{API}/lessons/non-existent")
        assert r.status_code == 404

    def test_years(self, session):
        r = session.get(f"{API}/years")
        assert r.status_code == 200
        years = r.json()
        assert isinstance(years, list) and len(years) > 0
        assert years == sorted(years, reverse=True)


# ----- Questions -----
class TestQuestions:
    def test_questions_filter(self, session):
        r = session.get(f"{API}/questions", params={
            "subtopic": "linear-equations", "year": 2019, "difficulty": "easy"
        })
        assert r.status_code == 200
        qs = r.json()
        assert len(qs) >= 1
        for q in qs:
            assert q["subtopic"] == "linear-equations"
            assert q["year"] == 2019
            assert q["difficulty"] == "easy"
            # answer should NOT be exposed in list view
            assert "answer" not in q
            assert "solution_steps" not in q
            assert len(q["options"]) > 0

    def test_questions_all(self, session):
        r = session.get(f"{API}/questions")
        assert r.status_code == 200
        assert len(r.json()) >= 50

    def test_question_detail(self, session):
        # find a known one
        r = session.get(f"{API}/questions", params={
            "subtopic": "linear-equations", "year": 2019, "difficulty": "easy"
        })
        qid = r.json()[0]["id"]
        r2 = session.get(f"{API}/questions/{qid}")
        assert r2.status_code == 200
        d = r2.json()
        assert "answer" in d and "solution_steps" in d
        assert isinstance(d["solution_steps"], list)

    def test_question_not_found(self, session):
        r = session.get(f"{API}/questions/non-existent-id")
        assert r.status_code == 404


# ----- Attempts / Progress -----
class TestAttemptsProgress:
    def test_attempt_correct_and_progress(self, session, auth_headers):
        # Get a known question
        r = session.get(f"{API}/questions", params={
            "subtopic": "linear-equations", "year": 2019, "difficulty": "easy"
        })
        q = r.json()[0]
        qid = q["id"]
        detail = session.get(f"{API}/questions/{qid}").json()
        correct_ans = detail["answer"]

        # Submit correct answer
        att = session.post(f"{API}/attempts", headers=auth_headers, json={
            "question_id": qid, "selected": correct_ans
        })
        assert att.status_code == 200
        ad = att.json()
        assert ad["correct"] is True
        assert ad["correct_answer"] == correct_ans
        assert isinstance(ad["solution_steps"], list) and len(ad["solution_steps"]) > 0

        # Wrong attempt
        wrong = "ZZZ_wrong"
        att2 = session.post(f"{API}/attempts", headers=auth_headers, json={
            "question_id": qid, "selected": wrong
        })
        assert att2.status_code == 200
        assert att2.json()["correct"] is False

        # Progress
        prog = session.get(f"{API}/progress", headers=auth_headers)
        assert prog.status_code == 200
        p = prog.json()
        assert p["total_attempts"] >= 2
        assert p["correct"] >= 1
        assert "by_subtopic" in p
        assert "linear-equations" in p["by_subtopic"]
        assert isinstance(p["recent_attempts"], list)
        if p["recent_attempts"]:
            assert "question_text" in p["recent_attempts"][0]
            assert "subtopic_name" in p["recent_attempts"][0]

    def test_attempt_requires_auth(self, session):
        r = session.post(f"{API}/attempts", json={"question_id": "x", "selected": "y"})
        assert r.status_code == 401


# ----- AI Tutor (Gemini 3 Flash) -----
class TestTutor:
    def test_tutor_chat(self, session, auth_headers):
        sid = f"test-{uuid.uuid4().hex[:8]}"
        r = session.post(f"{API}/tutor/chat", headers=auth_headers, json={
            "session_id": sid, "message": "Solve 2x + 7 = 19"
        }, timeout=60)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["session_id"] == sid
        assert isinstance(d["reply"], str) and len(d["reply"]) > 20
        # Should contain a step-style answer mentioning x = 6
        low = d["reply"].lower()
        assert "step" in low or "=" in d["reply"]

        # History
        h = session.get(f"{API}/tutor/history/{sid}", headers=auth_headers)
        assert h.status_code == 200
        msgs = h.json()
        assert len(msgs) >= 2
        roles = [m["role"] for m in msgs]
        assert "user" in roles and "assistant" in roles
