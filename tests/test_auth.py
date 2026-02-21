"""
Tests for authentication routes — Register, Login, Logout.
"""
from flask.testing import FlaskClient


class TestAuthRoutes:
    """Test auth blueprint routes."""

    def test_login_page_renders(self, client: FlaskClient) -> None:
        """GET /auth/login should return 200."""
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        assert b"Log In" in resp.data

    def test_register_page_renders(self, client: FlaskClient) -> None:
        """GET /auth/register should return 200."""
        resp = client.get("/auth/register")
        assert resp.status_code == 200
        assert b"Register" in resp.data

    def test_login_missing_fields_flashes_warning(self, client: FlaskClient) -> None:
        """POST /auth/login with empty fields should flash error."""
        resp = client.post("/auth/login", data={"email": "", "password": ""}, follow_redirects=True)
        assert resp.status_code == 200

    def test_register_short_password(self, client: FlaskClient) -> None:
        """POST /auth/register with short password should flash error."""
        resp = client.post("/auth/register", data={
            "name": "Test", "email": "test@test.com", "password": "123"
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b"at least 6 characters" in resp.data

    def test_logout_redirects(self, auth_client: FlaskClient) -> None:
        """GET /auth/logout should redirect to login."""
        resp = auth_client.get("/auth/logout")
        assert resp.status_code in (302, 303)

    def test_unauthenticated_dashboard_redirects(self, client: FlaskClient) -> None:
        """GET / without login should redirect to auth/login."""
        resp = client.get("/")
        assert resp.status_code in (302, 303)

    def test_authenticated_dashboard_renders(self, auth_client: FlaskClient) -> None:
        """GET / with session should render dashboard."""
        resp = auth_client.get("/")
        assert resp.status_code == 200
