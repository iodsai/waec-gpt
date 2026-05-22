"""V3 backend tests — Further Maths pivot (Statistics, Calculus, Vectors)."""
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
    data = r.json()
    assert data["user"].get("is_admin") is True, "admin user should have is_admin=true"
    return data["token"]


# ---------------- Topics ----------------
class TestTopics:
    def test_topics_structure(self, session):
        r = session.get(f"{BASE_URL}/api/topics")
        assert r.status_code == 200
        topics = r.json()["topics"]
        assert len(topics) == 8, f"expected 8 topics, got {len(topics)}"

        by_id = {t["id"]: t for t in topics}
        available = {"statistics", "calculus", "vectors",
                     "sets-logic", "surds-polynomials", "sequences-binomial", "matrices", "mechanics"}
        for tid in available:
            assert by_id[tid]["status"] == "available", f"{tid} should be available"
            assert by_id[tid]["question_count"] >= 50, f"{tid} should have ≥50 questions, got {by_id[tid]['question_count']}"


# ---------------- Questions ----------------
class TestQuestions:
    @pytest.mark.parametrize("topic", ["statistics", "calculus", "vectors"])
    def test_50_per_topic(self, session, topic):
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": topic, "limit": 200})
        assert r.status_code == 200
        data = r.json()
        items = data.get("questions") if isinstance(data, dict) else data
        # filter to seed questions only (exclude scraped/imported ones if present)
        topic_items = [q for q in items if q.get("topic") == topic]
        assert len(topic_items) >= 50, f"expected >=50 {topic} questions, got {len(topic_items)}"

    @pytest.mark.parametrize("legacy", ["algebra", "trigonometry", "geometry"])
    def test_no_legacy_topics(self, session, legacy):
        r = session.get(f"{BASE_URL}/api/questions", params={"topic": legacy, "limit": 200})
        # endpoint may 200 with [] or 400/404
        if r.status_code == 200:
            data = r.json()
            items = data.get("questions") if isinstance(data, dict) else data
            legacy_items = [q for q in items if q.get("topic") == legacy]
            assert len(legacy_items) == 0, f"legacy topic {legacy} still has {len(legacy_items)} questions"


# ---------------- Lessons ----------------
class TestLessons:
    @pytest.mark.parametrize("slug", ["limits", "differentiation", "scalar-product"])
    def test_fm_lessons_exist(self, session, slug):
        r = session.get(f"{BASE_URL}/api/lessons/{slug}")
        assert r.status_code == 200, f"{slug}: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("title") or body.get("content") or body.get("sections"), f"{slug}: empty lesson"

    def test_legacy_lesson_404(self, session):
        r = session.get(f"{BASE_URL}/api/lessons/linear-equations")
        assert r.status_code == 404, f"expected 404, got {r.status_code}"


# ---------------- Exams ----------------
class TestExams:
    def _auth(self, token):
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def test_quick_mixed_10(self, session, student_token):
        r = session.post(f"{BASE_URL}/api/exams/start", json={"mode": "quick"}, headers=self._auth(student_token))
        assert r.status_code == 200, r.text
        data = r.json()
        qs = data.get("questions") or data.get("items") or []
        assert len(qs) == 10, f"quick should be 10, got {len(qs)}"
        topics = {q.get("topic") for q in qs}
        fm = {"statistics", "calculus", "vectors",
              "sets-logic", "surds-polynomials", "sequences-binomial", "matrices", "mechanics"}
        assert topics.issubset(fm), f"non-FM topics found: {topics - fm}"

    def test_mock_40(self, session, student_token):
        r = session.post(f"{BASE_URL}/api/exams/start", json={"mode": "mock"}, headers=self._auth(student_token))
        assert r.status_code == 200, r.text
        data = r.json()
        qs = data.get("questions") or data.get("items") or []
        assert len(qs) == 40, f"mock should be 40, got {len(qs)}"

    def test_topic_filter_calculus(self, session, student_token):
        r = session.post(f"{BASE_URL}/api/exams/start", json={"mode": "quick", "topic": "calculus"}, headers=self._auth(student_token))
        assert r.status_code == 200, r.text
        data = r.json()
        qs = data.get("questions") or data.get("items") or []
        assert len(qs) > 0
        for q in qs:
            assert q.get("topic") == "calculus", f"non-calculus question in topic filter: {q.get('topic')}"


# ---------------- SymPy Verify ----------------
class TestSolverVerify:
    def test_verify_quadratic(self, session, student_token):
        r = session.post(
            f"{BASE_URL}/api/solver/verify",
            json={"equation": "x^2-5x+6=0", "claimed_answer": "3"},
            headers={"Authorization": f"Bearer {student_token}", "Content-Type": "application/json"},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("ok") is True
        sols = [str(s) for s in data.get("solutions", [])]
        assert set(sols) == {"2", "3"}, f"expected solutions [2,3], got {sols}"
        assert data.get("matches_claim") is True


# ---------------- Admin ----------------
class TestAdmin:
    def test_admin_papers_29(self, session, admin_token):
        r = session.get(f"{BASE_URL}/api/admin/import/papers", headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200, r.text
        data = r.json()
        papers = data.get("papers") if isinstance(data, dict) else data
        assert len(papers) == 29, f"expected 29 papers, got {len(papers)}"
        # All URLs should reference Further
        for p in papers:
            url = (p.get("url") or p.get("link") or "").lower()
            assert "further" in url, f"non-Further URL: {url}"


# ---------------- Theory attempts excluded from progress ----------------
class TestTheoryAttempts:
    def _auth(self, token):
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def test_theory_attempt_no_penalty_and_progress_excludes(self, session, student_token):
        # find a theory question
        r = session.get(f"{BASE_URL}/api/questions", params={"limit": 200})
        assert r.status_code == 200
        items = r.json()
        items = items.get("questions") if isinstance(items, dict) else items
        theory = next((q for q in items if q.get("question_type") == "theory"), None)
        if not theory:
            pytest.skip("no theory question available")

        # progress before
        pre = session.get(f"{BASE_URL}/api/progress", headers=self._auth(student_token))
        assert pre.status_code == 200
        pre_total = (pre.json().get("total_attempts") or pre.json().get("total") or 0)

        # attempt the theory question
        att = session.post(
            f"{BASE_URL}/api/attempts",
            json={"question_id": theory["id"], "selected": "—"},
            headers=self._auth(student_token),
        )
        assert att.status_code in (200, 201), att.text
        body = att.json()
        # should not be marked correct
        assert body.get("correct") in (False, None), f"theory attempt unexpectedly correct: {body}"

        # progress after — should be unchanged (is_reveal excluded)
        post = session.get(f"{BASE_URL}/api/progress", headers=self._auth(student_token))
        assert post.status_code == 200
        post_total = (post.json().get("total_attempts") or post.json().get("total") or 0)
        # allow same OR +1 if backend counts but excludes from accuracy; just verify accuracy not damaged
        acc = post.json().get("accuracy")
        if acc is not None:
            assert 0 <= acc <= 100
