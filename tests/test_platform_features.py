"""
Tests for platform features — History, Gamification, Learning, Admin,
Job Match, Classroom, Digest, and Smart Career Search.
"""
from flask.testing import FlaskClient
from unittest.mock import patch


class TestHistoryRoutes:
    """Test history + bookmarks blueprint."""

    @patch("app.history.routes.get_user_queries", return_value=[])
    def test_history_index_renders(self, mock_get: object, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/history/")
        assert resp.status_code == 200

    @patch("app.history.routes.get_user_bookmarks", return_value=[])
    def test_bookmarks_renders(self, mock_get: object, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/history/bookmarks")
        assert resp.status_code == 200

    def test_history_unauthenticated(self, client: FlaskClient) -> None:
        resp = client.get("/history/")
        assert resp.status_code in (302, 303)


class TestGamificationRoutes:
    """Test gamification blueprint."""

    @patch("app.gamification.routes.get_user_badges", return_value=[])
    @patch("app.gamification.routes.get_leaderboard", return_value=[])
    def test_gamification_renders(self, mock_lb: object, mock_badges: object, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/gamification/")
        assert resp.status_code == 200


class TestLearningRoutes:
    """Test learning blueprint."""

    def test_learning_get_renders(self, auth_client: FlaskClient) -> None:
        with patch("app.learning.routes.get_user_progress", return_value=None):
            resp = auth_client.get("/learning/")
            assert resp.status_code == 200

    @patch("app.learning.routes.generate_learning_path", return_value="Mock roadmap")
    @patch("app.learning.routes.save_query")
    @patch("app.learning.routes.save_user_progress")
    def test_learning_post(self, mock_prog: object, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/learning/", data={
            "career_goal": "ML Engineer", "current_skills": "Python", "timeframe": "6 months"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestJobMatchRoutes:
    """Test job match / smart career search blueprint."""

    def test_job_match_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/job-match/")
        assert resp.status_code == 200

    @patch("app.job_match.routes.smart_career_search", return_value=("Mock result", [{"title": "Test", "url": "https://example.com"}]))
    @patch("app.job_match.routes.save_query")
    def test_job_match_post(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/job-match/", data={"question": "Python developer salary in India"}, follow_redirects=True)
        assert resp.status_code == 200


class TestClassroomRoutes:
    """Test classroom blueprint."""

    @patch("app.classroom.routes.get_user_classrooms", return_value=[])
    def test_classroom_index_renders(self, mock_get: object, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/classroom/")
        assert resp.status_code == 200

    def test_classroom_unauthenticated(self, client: FlaskClient) -> None:
        resp = client.get("/classroom/")
        assert resp.status_code in (302, 303)


class TestDigestRoutes:
    """Test digest blueprint."""

    @patch("app.digest.routes.get_digest_prefs", return_value=None)
    def test_digest_get_renders(self, mock_get: object, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/digest/")
        assert resp.status_code == 200


class TestAdminRoutes:
    """Test admin blueprint."""

    def test_admin_requires_admin_role(self, auth_client: FlaskClient) -> None:
        """Regular user should be redirected from admin."""
        resp = auth_client.get("/admin/")
        assert resp.status_code in (302, 303)

    @patch("app.admin.routes.get_all_users", return_value=[])
    @patch("app.admin.routes.get_all_queries", return_value=[])
    def test_admin_renders_for_admin(self, mock_q: object, mock_u: object, admin_client: FlaskClient) -> None:
        resp = admin_client.get("/admin/")
        assert resp.status_code == 200
