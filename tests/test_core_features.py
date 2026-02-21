"""
Tests for core AI feature routes — Career, Courses, Insights.
"""
from flask.testing import FlaskClient
from unittest.mock import patch


class TestCareerRoutes:
    """Test career blueprint."""

    def test_career_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/career/")
        assert resp.status_code == 200

    @patch("app.career.routes.generate_career_overview", return_value="Mock career overview")
    @patch("app.career.routes.save_query")
    def test_career_post_returns_result(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/career/", data={"career_field": "Software Engineering"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_career_unauthenticated_redirects(self, client: FlaskClient) -> None:
        resp = client.get("/career/")
        assert resp.status_code in (302, 303)


class TestCoursesRoutes:
    """Test courses blueprint."""

    def test_courses_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/courses/")
        assert resp.status_code == 200

    @patch("app.courses.routes.generate_course_recommendations", return_value="Mock courses")
    @patch("app.courses.routes.save_query")
    def test_courses_post_returns_result(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/courses/", data={
            "interest": "Python", "skill_level": "beginner", "goal": "Get a job"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestInsightsRoutes:
    """Test insights blueprint."""

    def test_insights_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/insights/")
        assert resp.status_code == 200

    @patch("app.insights.routes.generate_market_insights", return_value="Mock insights")
    @patch("app.insights.routes.save_query")
    def test_insights_post_returns_result(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/insights/", data={"industry": "Technology"}, follow_redirects=True)
        assert resp.status_code == 200
