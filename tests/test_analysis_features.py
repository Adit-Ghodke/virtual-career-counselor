"""
Tests for analysis features — Pivot, Trends, Peers, Skill Gap, GitHub Analyzer.
"""
from flask.testing import FlaskClient
from unittest.mock import patch


class TestPivotRoutes:
    """Test pivot blueprint."""

    def test_pivot_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/pivot/")
        assert resp.status_code == 200

    @patch("app.pivot.routes.analyze_career_pivot", return_value="Mock pivot analysis")
    @patch("app.pivot.routes.save_query")
    def test_pivot_post(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/pivot/", data={
            "current_role": "Teacher", "target_role": "Data Scientist",
            "experience_years": "5", "skills": "Python, SQL"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestTrendsRoutes:
    """Test trends blueprint."""

    def test_trends_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/trends/")
        assert resp.status_code == 200

    @patch("app.trends.routes.generate_trends_report", return_value="Mock trends")
    @patch("app.trends.routes.save_query")
    def test_trends_post(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/trends/", data={"industries": ["Technology"]}, follow_redirects=True)
        assert resp.status_code == 200


class TestPeersRoutes:
    """Test peers blueprint."""

    def test_peers_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/peers/")
        assert resp.status_code == 200

    @patch("app.peers.routes.generate_peer_comparison", return_value="Mock comparison")
    @patch("app.peers.routes.save_query")
    @patch("app.peers.routes.award_badge")
    def test_peers_post(self, mock_badge: object, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/peers/", data={
            "role": "SWE", "experience": "3", "skills": "Python",
            "location": "India", "education": "B.Tech"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestSkillGapRoutes:
    """Test skill gap blueprint."""

    def test_skill_gap_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/skill-gap/")
        assert resp.status_code == 200

    @patch("app.skill_gap.routes.analyze_skill_gap", return_value='{"summary":"Mock","categories":[],"scores":[]}')
    @patch("app.skill_gap.routes.save_query")
    def test_skill_gap_post(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/skill-gap/", data={
            "current_skills": "Python, Flask",
            "target_role": "ML Engineer"
        }, follow_redirects=True)
        assert resp.status_code == 200


class TestGitHubAnalyzerRoutes:
    """Test GitHub analyzer blueprint."""

    def test_github_get_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/github/")
        assert resp.status_code == 200

    def test_github_unauthenticated(self, client: FlaskClient) -> None:
        resp = client.get("/github/")
        assert resp.status_code in (302, 303)
