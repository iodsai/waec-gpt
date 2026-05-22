"""V2.2 tests: theory question_type support + waeconline imports."""
import os
import random
import string
import pytest
import requests

BASE = os.environ.get("REACT_APP_BACKEND_URL", "https://mathmastery-waec.preview.emergentagent.com").rstrip("/")
API = f"{BASE}/api"


def _rand(n=6):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


@pytest.fixture(scope="module")
def student_token():
    r = requests.post(f"{API}/auth/login", json={"email": "student@waec.com", "password": "Student@123"})
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def admin_token():
    r = requests.post(f"{API}/auth/login", json={"email": "admin@waec.com", "password": "Admin@123"})
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def auth_student(student_token):
    return {"Authorization": f"Bearer {student_token}"}


@pytest.fixture(scope="module")
def auth_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# ===== /api/questions includes question_type =====
def test_list_questions_has_question_type():
    r = requests.get(f"{API}/questions", params={"limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) > 0
    for q in items:
        assert "question_type" in q
        assert q["question_type"] in ("objective", "theory")


def test_get_question_detail_has_question_type():
    r = requests.get(f"{API}/questions", params={"limit": 1})
    qid = r.json()[0]["id"]
    d = requests.get(f"{API}/questions/{qid}").json()
    assert "question_type" in d
    assert "answer" in d and "solution_steps" in d


# ===== Theory questions have options=[] and non-empty answer+solution =====
def test_theory_questions_shape(auth_student):
    # find a theory question via list endpoint (scan many)
    r = requests.get(f"{API}/questions", params={"limit": 500})
    items = r.json()
    theory_items = [q for q in items if q.get("question_type") == "theory"]
    assert len(theory_items) > 0, "Expected at least one theory question in DB"
    sample = theory_items[0]
    assert sample["options"] == []
    d = requests.get(f"{API}/questions/{sample['id']}").json()
    assert d["question_type"] == "theory"
    assert d["options"] == []
    assert d["answer"], "Theory question must have non-empty answer"
    assert isinstance(d["solution_steps"], list) and len(d["solution_steps"]) > 0


# ===== POST /attempts on theory works =====
def test_attempt_on_theory_returns_solution(auth_student):
    r = requests.get(f"{API}/questions", params={"limit": 500}).json()
    theory_items = [q for q in r if q.get("question_type") == "theory"]
    assert theory_items
    qid = theory_items[0]["id"]
    resp = requests.post(f"{API}/attempts",
                         json={"question_id": qid, "selected": "—"},
                         headers=auth_student)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "correct_answer" in body and body["correct_answer"]
    assert isinstance(body["solution_steps"], list) and len(body["solution_steps"]) > 0


# ===== Exam start excludes theory =====
@pytest.mark.parametrize("run", range(3))
def test_exam_start_excludes_theory(auth_student, run):
    resp = requests.post(f"{API}/exams/start",
                         json={"mode": "quick"},
                         headers=auth_student)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["questions"]) == 10
    for q in body["questions"]:
        assert q["options"] and len(q["options"]) >= 2, f"Exam returned a question with no/few options (likely theory): {q}"


# ===== Admin save accepts theory payload without options =====
def test_admin_save_theory_no_options(auth_admin):
    payload = {
        "paper_url": f"https://test/{_rand()}",
        "year": 2099,
        "questions": [{
            "subtopic": "linear-equations",
            "difficulty": "medium",
            "question": f"TEST_THEORY_{_rand()}: Prove something interesting.",
            "options": [],
            "question_type": "theory",
            "answer": "QED",
            "solution_steps": ["Step 1: setup", "Step 2: conclude"],
        }]
    }
    r = requests.post(f"{API}/admin/import/save", json=payload, headers=auth_admin)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["saved"] == 1
    qid = data["ids"][0]
    # verify persistence
    d = requests.get(f"{API}/questions/{qid}").json()
    assert d["question_type"] == "theory"
    assert d["options"] == []
    # cleanup
    requests.delete(f"{API}/admin/questions/{qid}", headers=auth_admin)


# ===== Admin save rejects objective payload with <2 options =====
def test_admin_save_rejects_objective_with_too_few_options(auth_admin):
    payload = {
        "paper_url": f"https://test/{_rand()}",
        "year": 2099,
        "questions": [{
            "subtopic": "linear-equations",
            "difficulty": "medium",
            "question": f"TEST_BAD_{_rand()}: bad objective",
            "options": ["only one"],
            "question_type": "objective",
            "answer": "only one",
            "solution_steps": ["x"],
        }]
    }
    r = requests.post(f"{API}/admin/import/save", json=payload, headers=auth_admin)
    # all skipped -> 400 "No valid questions"
    assert r.status_code == 400, r.text


# ===== ~62 real waeconline-source questions exist (2019-2023) =====
def test_waeconline_imported_questions_exist(auth_admin):
    r = requests.get(f"{API}/admin/questions", headers=auth_admin)
    assert r.status_code == 200
    all_q = r.json()
    waec_q = [q for q in all_q if q.get("source") == "waeconline"]
    years = sorted({q["year"] for q in waec_q})
    assert len(waec_q) >= 40, f"Expected ~62 waeconline questions, got {len(waec_q)}"
    # ensure years are within 2019-2023
    for y in years:
        assert 2019 <= y <= 2023, f"Unexpected year for waeconline import: {y}"


# ===== Admin papers catalog has ~26 entries =====
def test_admin_papers_catalog(auth_admin):
    r = requests.get(f"{API}/admin/import/papers", headers=auth_admin)
    assert r.status_code == 200
    papers = r.json()["papers"]
    assert len(papers) >= 20, f"Expected >=20 papers, got {len(papers)}"
