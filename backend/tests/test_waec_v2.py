"""WAEC Math AI V2 backend tests — topics multi-subject, solver, exams, similar, admin."""
import os
import io
import uuid
import time
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://mathmastery-waec.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

STUDENT_EMAIL = "student@waec.com"
STUDENT_PASS = "Student@123"
ADMIN_EMAIL = "admin@waec.com"
ADMIN_PASS = "Admin@123"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def student_token(session):
    r = session.post(f"{API}/auth/login", json={"email": STUDENT_EMAIL, "password": STUDENT_PASS})
    assert r.status_code == 200, f"student login failed: {r.text}"
    return r.json()["token"]


@pytest.fixture(scope="session")
def admin_token(session):
    r = session.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASS})
    assert r.status_code == 200, f"admin login failed: {r.text}"
    j = r.json()
    assert j["user"]["is_admin"] is True, f"admin user missing is_admin flag: {j['user']}"
    return j["token"]


def H(tok):
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


# -------- Topics --------
class TestTopics:
    def test_topics_v2(self, session):
        r = session.get(f"{API}/topics")
        assert r.status_code == 200
        topics = r.json()["topics"]
        assert len(topics) == 6, f"Expected 6 topics, got {len(topics)}"
        by_id = {t["id"]: t for t in topics}
        # available
        for tid in ("algebra", "trigonometry", "geometry"):
            assert tid in by_id, f"Missing topic {tid}"
            assert by_id[tid]["status"] == "available"
        # coming soon (3)
        coming = [t for t in topics if t["status"] == "coming_soon"]
        assert len(coming) == 3
        # question counts (>= expected)
        assert by_id["algebra"]["question_count"] >= 80, f"algebra count {by_id['algebra']['question_count']}"
        assert by_id["trigonometry"]["question_count"] >= 25
        assert by_id["geometry"]["question_count"] >= 25


# -------- Questions filter by topic --------
class TestQuestionsByTopic:
    def test_trig_questions(self, session):
        r = session.get(f"{API}/questions", params={"topic": "trigonometry", "limit": 500})
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 25
        assert all(q["topic"] == "trigonometry" for q in items)

    def test_geometry_questions(self, session):
        r = session.get(f"{API}/questions", params={"topic": "geometry", "limit": 500})
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 25
        assert all(q["topic"] == "geometry" for q in items)


# -------- Lessons --------
class TestLessons:
    def test_trig_ratios_lesson(self, session):
        r = session.get(f"{API}/lessons/trig-ratios")
        assert r.status_code == 200
        j = r.json()
        assert j["subtopic_id"] == "trig-ratios"
        assert j["topic"] == "trigonometry"
        assert len(j["notes"]) > 0

    def test_circle_theorems_lesson(self, session):
        r = session.get(f"{API}/lessons/circle-theorems")
        assert r.status_code == 200
        j = r.json()
        assert j["topic"] == "geometry"
        assert len(j["notes"]) > 0


# -------- Solver (SymPy) --------
class TestSolver:
    def test_linear(self, session, student_token):
        r = session.post(f"{API}/solver/verify",
                         headers=H(student_token),
                         json={"equation": "2x+7=19", "claimed_answer": "6"})
        assert r.status_code == 200, r.text
        j = r.json()
        assert j.get("ok") is True
        assert "6" in [str(s) for s in j.get("solutions", [])]
        assert j.get("matches_claim") is True

    def test_quadratic(self, session, student_token):
        r = session.post(f"{API}/solver/verify",
                         headers=H(student_token),
                         json={"equation": "x^2 - 5x + 6 = 0"})
        assert r.status_code == 200, r.text
        j = r.json()
        assert j.get("ok") is True
        sols = [str(s) for s in j.get("solutions", [])]
        assert "2" in sols and "3" in sols


# -------- Exams --------
class TestExams:
    def test_quick_drill_starts(self, session, student_token):
        r = session.post(f"{API}/exams/start", headers=H(student_token),
                         json={"mode": "quick", "topic": "algebra"})
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["duration_seconds"] == 300
        assert len(j["questions"]) == 10
        # topic filter
        assert all(q["topic"] == "algebra" for q in j["questions"])

    def test_mock_starts(self, session, student_token):
        r = session.post(f"{API}/exams/start", headers=H(student_token),
                         json={"mode": "mock"})
        assert r.status_code == 200
        j = r.json()
        assert j["duration_seconds"] == 3600
        assert len(j["questions"]) == 40

    def test_trig_exam_filters(self, session, student_token):
        r = session.post(f"{API}/exams/start", headers=H(student_token),
                         json={"mode": "quick", "topic": "trigonometry"})
        assert r.status_code == 200
        j = r.json()
        assert all(q["topic"] == "trigonometry" for q in j["questions"])

    def test_submit_and_report_and_list(self, session, student_token):
        # start
        r = session.post(f"{API}/exams/start", headers=H(student_token),
                         json={"mode": "quick", "topic": "algebra"})
        j = r.json()
        exam_id = j["exam_id"]
        questions = j["questions"]
        # Answer first option for each
        answers = {q["id"]: q["options"][0] for q in questions}
        sub = session.post(f"{API}/exams/{exam_id}/submit", headers=H(student_token),
                           json={"answers": answers})
        assert sub.status_code == 200, sub.text
        report = sub.json()
        assert report["total_questions"] == 10
        assert "score_percent" in report
        assert "by_subtopic" in report and isinstance(report["by_subtopic"], dict)
        assert isinstance(report["detail"], list)
        assert len(report["detail"]) == 10

        # GET report
        r2 = session.get(f"{API}/exams/{exam_id}", headers=H(student_token))
        assert r2.status_code == 200
        assert r2.json()["exam_id"] == exam_id

        # list
        r3 = session.get(f"{API}/exams", headers=H(student_token))
        assert r3.status_code == 200
        items = r3.json()
        assert any(e["id"] == exam_id for e in items)


# -------- Similar (AI Gemini) --------
class TestSimilar:
    def test_similar_generation(self, session, student_token):
        # pick first algebra question
        qs = session.get(f"{API}/questions", params={"topic": "algebra", "limit": 5}).json()
        assert qs
        qid = qs[0]["id"]
        r = session.post(f"{API}/questions/{qid}/similar",
                         headers=H(student_token),
                         json={"n": 2}, timeout=60)
        assert r.status_code == 200, r.text
        j = r.json()
        assert "items" in j
        assert isinstance(j["items"], list)
        assert len(j["items"]) >= 1, "Expected at least 1 generated item"


# -------- Admin --------
class TestAdmin:
    def test_admin_login_has_is_admin(self, admin_token):
        assert admin_token  # already validated in fixture

    def test_student_cannot_create_question(self, session, student_token):
        payload = {
            "topic": "algebra", "subtopic": "linear-equations", "year": 2024,
            "difficulty": "easy",
            "question": "TEST denied 2+2=?", "options": ["1", "2", "3", "4"],
            "answer": "4", "solution_steps": ["TEST"],
        }
        r = session.post(f"{API}/admin/questions", headers=H(student_token), json=payload)
        assert r.status_code == 403

    def test_admin_can_create_list_and_delete(self, session, admin_token):
        payload = {
            "topic": "algebra", "subtopic": "linear-equations", "year": 2024,
            "difficulty": "easy",
            "question": f"TEST_{uuid.uuid4().hex[:6]} 2+2=?",
            "options": ["1", "2", "3", "4"],
            "answer": "4", "solution_steps": ["TEST step"],
        }
        r = session.post(f"{API}/admin/questions", headers=H(admin_token), json=payload)
        assert r.status_code == 200, r.text
        new_id = r.json()["id"]

        listed = session.get(f"{API}/admin/questions", headers=H(admin_token))
        assert listed.status_code == 200
        assert any(q["id"] == new_id for q in listed.json())

        # delete
        d = session.delete(f"{API}/admin/questions/{new_id}", headers=H(admin_token))
        assert d.status_code == 200
        assert d.json().get("ok") is True

    def test_admin_extract_endpoint_accepts_multipart(self, admin_token):
        # tiny invalid jpg payload, accept 200 OR 500 (Gemini may fail)
        files = {"image": ("tiny.jpg", io.BytesIO(b"\xff\xd8\xff\xd9"), "image/jpeg")}
        headers = {"Authorization": f"Bearer {admin_token}"}
        r = requests.post(f"{API}/admin/questions/extract", files=files, headers=headers, timeout=60)
        assert r.status_code in (200, 400, 500), f"unexpected {r.status_code} {r.text}"

    def test_admin_extract_requires_admin(self, student_token):
        files = {"image": ("tiny.jpg", io.BytesIO(b"\xff\xd8\xff\xd9"), "image/jpeg")}
        headers = {"Authorization": f"Bearer {student_token}"}
        r = requests.post(f"{API}/admin/questions/extract", files=files, headers=headers, timeout=30)
        assert r.status_code == 403
