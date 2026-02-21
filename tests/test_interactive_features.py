"""
Tests for interactive AI features — Negotiation, Interview, Cover Letter, Resume.
"""
from flask.testing import FlaskClient
from unittest.mock import patch


class TestNegotiationRoutes:
    """Test negotiation blueprint."""

    def test_negotiation_start_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/negotiation/")
        assert resp.status_code == 200

    @patch("app.negotiation.routes.negotiation_reply", return_value="Mock negotiation reply")
    @patch("app.negotiation.routes.save_conversation")
    def test_negotiation_begin(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/negotiation/begin", data={
            "job_title": "Software Engineer", "current_salary": "80000",
            "target_salary": "100000", "experience_years": "5"
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_negotiation_unauthenticated(self, client: FlaskClient) -> None:
        resp = client.get("/negotiation/")
        assert resp.status_code in (302, 303)


class TestInterviewRoutes:
    """Test interview blueprint."""

    def test_interview_start_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/interview/")
        assert resp.status_code == 200

    @patch("app.interview.routes.interview_reply", return_value="Mock interview question")
    @patch("app.interview.routes.save_conversation")
    def test_interview_begin(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/interview/begin", data={
            "company": "Google", "role": "SWE", "experience": "3"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestCoverLetterRoutes:
    """Test cover letter blueprint."""

    def test_cover_letter_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/cover-letter/")
        assert resp.status_code == 200

    @patch("app.cover_letter.routes.generate_cover_letter", return_value="Mock cover letter")
    @patch("app.cover_letter.routes.save_query")
    def test_cover_letter_post(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/cover-letter/", data={
            "company_name": "Google",
            "job_description": "Looking for a Python developer",
            "resume_text": "5 years experience",
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_cover_letter_missing_fields(self, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/cover-letter/", data={
            "company_name": "", "job_description": ""
        }, follow_redirects=True)
        assert resp.status_code == 200  # re-renders form with flash


class TestResumeRoutes:
    """Test resume blueprint."""

    def test_resume_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/resume/")
        assert resp.status_code == 200

    def test_resume_unauthenticated(self, client: FlaskClient) -> None:
        resp = client.get("/resume/")
        assert resp.status_code in (302, 303)
