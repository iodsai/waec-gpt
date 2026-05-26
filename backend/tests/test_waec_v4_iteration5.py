"""Iteration 5 backend tests — 5 new topics activation, batch import endpoints, new lessons."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://mathmastery-waec.preview.emergentagent.com").rstrip("/")


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def student_token(session):
    r = session.post(f"{BASE_URL}/api/auth/login", json={"email": "student@waec.com", "password": "Student@123"})
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def admin_token(session):
    r = session.post(f"{BASE_URL}/api/auth/login", json={"email": "admin@waec.com", "password": "Admin@123"})
    assert r.status_code == 200, r.text
    return r.json()["token"]


# ---------------- All 8 topics now available ----------------
class TestAllTopicsAvailable:
    def test_all_8_topics_available(self, session):
        r = session.get(f"{BASE_URL}/api/topics")
        assert r.status_code == 200
        topics = r.json()["topics"]
        assert len(topics) == 8
        by_id = {t["id"]: t for t in topics}
        new_topics = ["sets-logic", "surds-polynomials", "sequences-binomial", "matrices", "mechanics"]
        for tid in new_topics:
            assert tid in by_id, f"missing topic id {tid}"
            assert by_id[tid]["status"] == "available", f"{tid} status={by_id[tid]['status']}, expected 'available'"
            assert by_id[tid]["question_count"] >= 50, f"{tid} only has {by_id[tid]['question_count']} questions"


# ---------------- 50 questions per new topic ----------------
class TestNewTopicQuestionCounts:
    @pytest.mark.parametrize("topic", ["sets-logic", "surds-polynomials", "sequences-binomial", "matrices", "mechanics"])
    def test_50_q_per_new_topic(self, session, topic):
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": topic, "limit": 200})
        assert r.status_code == 200
        data = r.json()
        items = data.get("questions") if isinstance(data, dict) else data
        topic_items = [q for q in items if q.get("topic") == topic]
        assert len(topic_items) >= 50, f"expected >=50 {topic} questions, got {len(topic_items)}"


# ---------------- Lessons for new topics ----------------
class TestNewLessons:
    @pytest.mark.parametrize("slug", ["set-operations", "kinematics"])
    def test_new_lessons_exist(self, session, slug):
        r = session.get(f"{BASE_URL}/api/lessons/{slug}")
        assert r.status_code == 200, f"{slug}: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("title") or body.get("content") or body.get("sections"), f"{slug}: empty lesson"


# ---------------- Quick Exam from new topics ----------------
class TestQuickExamNewTopics:
    @pytest.mark.parametrize("topic", ["matrices", "mechanics", "sets-logic", "surds-polynomials", "sequences-binomial"])
    def test_quick_from_new_topic(self, session, student_token, topic):
        r = session.post(
            f"{BASE_URL}/api/exams/start",
            json={"mode": "quick", "topic": topic},
            headers={"Authorization": f"Bearer {student_token}", "Content-Type": "application/json"},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        qs = data.get("questions") or data.get("items") or []
        assert len(qs) == 10, f"{topic} quick should be 10, got {len(qs)}"
        for q in qs:
            assert q.get("topic") == topic, f"non-{topic} question in filter: {q.get('topic')}"


# ---------------- Question filters via query params ----------------
class TestQuestionFilters:
    def test_filter_by_subtopic(self, session):
        # get list of subtopics for matrices
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": "matrices", "limit": 50})
        assert r.status_code == 200
        items = r.json()
        items = items.get("questions") if isinstance(items, dict) else items
        subs = {q.get("subtopic") for q in items if q.get("subtopic")}
        if subs:
            sub = next(iter(subs))
            r2 = session.get(f"{BASE_URL}/api/questions", params={"topic": "matrices", "subtopic": sub, "limit": 50})
            assert r2.status_code == 200
            items2 = r2.json()
            items2 = items2.get("questions") if isinstance(items2, dict) else items2
            for q in items2:
                assert q.get("subtopic") == sub


# ---------------- Admin batch import GET endpoints ----------------
class TestAdminBatchImport:
    def test_list_batch_jobs(self, session, admin_token):
        r = session.get(f"{BASE_URL}/api/admin/import/batch",
                        headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200, r.text
        data = r.json()
        jobs = data.get("jobs")
        assert isinstance(jobs, list), "jobs should be a list"
        # Just verify endpoint works; record count for context
        print(f"\nFound {len(jobs)} batch import jobs")
        for j in jobs[:5]:
            print(f"  - {j.get('id')}: status={j.get('status')} imported={j.get('imported_count')}")

    def test_completed_jobs_exist(self, session, admin_token):
        r = session.get(f"{BASE_URL}/api/admin/import/batch",
                        headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200
        jobs = r.json().get("jobs", [])
        completed = [j for j in jobs if j.get("status") == "completed"]
        # Per problem statement: 188 (2010-2018) + 88 (2019-2023) = 276 questions imported
        assert len(completed) >= 1, f"expected at least 1 completed job, got {len(completed)}"
        total_imported = sum(j.get("imported_count", 0) for j in completed)
        print(f"\nCompleted jobs: {len(completed)}, total questions imported: {total_imported}")

    def test_get_batch_job_by_id(self, session, admin_token):
        r = session.get(f"{BASE_URL}/api/admin/import/batch",
                        headers={"Authorization": f"Bearer {admin_token}"})
        jobs = r.json().get("jobs", [])
        if not jobs:
            pytest.skip("no batch jobs to fetch by id")
        job_id = jobs[0].get("id")
        r2 = session.get(f"{BASE_URL}/api/admin/import/batch/{job_id}",
                         headers={"Authorization": f"Bearer {admin_token}"})
        assert r2.status_code == 200, r2.text
        body = r2.json()
        assert body.get("id") == job_id

    def test_get_batch_job_404(self, session, admin_token):
        r = session.get(f"{BASE_URL}/api/admin/import/batch/nonexistent-job-id",
                        headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 404

    def test_batch_endpoint_requires_admin(self, session, student_token):
        r = session.get(f"{BASE_URL}/api/admin/import/batch",
                        headers={"Authorization": f"Bearer {student_token}"})
        assert r.status_code in (401, 403), f"student should not access admin endpoint, got {r.status_code}"


# ---------------- Attempts flow for ObjectivePane ----------------
class TestObjectiveAttempts:
    def test_objective_attempt_correct(self, session, student_token):
        # fetch a matrices question, submit its correct answer
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": "matrices", "limit": 5})
        items = r.json()
        items = items.get("questions") if isinstance(items, dict) else items
        q = next((x for x in items if x.get("question_type") == "objective" and x.get("correct_answer")), None)
        if not q:
            pytest.skip("no objective matrices question with correct_answer")
        r2 = session.post(
            f"{BASE_URL}/api/attempts",
            json={"question_id": q["id"], "selected": q["correct_answer"]},
            headers={"Authorization": f"Bearer {student_token}", "Content-Type": "application/json"},
        )
        assert r2.status_code in (200, 201), r2.text
        body = r2.json()
        assert body.get("correct") is True

    def test_similar_questions_endpoint(self, session, student_token):
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": "mechanics", "limit": 1})
        items = r.json()
        items = items.get("questions") if isinstance(items, dict) else items
        if not items:
            pytest.skip("no mechanics question")
        qid = items[0]["id"]
        r2 = session.post(f"{BASE_URL}/api/questions/{qid}/similar",
                          json={"n": 2},
                          headers={"Authorization": f"Bearer {student_token}",
                                   "Content-Type": "application/json"})
        assert r2.status_code == 200, r2.text
        data = r2.json()
        sim = data.get("questions") or data.get("similar") or data.get("items") or []
        assert isinstance(sim, list)
        assert data.get("count") == len(sim)
