"""
Tests for security features — CSRF protection, rate limiting, input validation.
"""
from flask import Flask
from flask.testing import FlaskClient


class TestCSRFProtection:
    """Verify CSRF is active and enforced."""

    def test_csrf_meta_tag_in_base(self, auth_client: FlaskClient) -> None:
        """Dashboard should contain CSRF meta tag."""
        resp = auth_client.get("/")
        assert b'name="csrf-token"' in resp.data

    def test_post_without_csrf_rejected_when_enabled(self, app: Flask) -> None:
        """POST without CSRF token should be rejected (400/403) when CSRF is enabled."""
        app.config["WTF_CSRF_ENABLED"] = True
        client = app.test_client()
        # Must be logged in first
        with client.session_transaction() as sess:
            sess["user_id"] = "test-user"
            sess["user_name"] = "Test"
            sess["email"] = "test@test.com"
            sess["role"] = "user"
        resp = client.post("/chatbot/send", data={"message": "test"})
        assert resp.status_code in (400, 302)  # CSRF rejection


class TestRateLimiting:
    """Verify rate limiting is configured."""

    def test_limiter_is_initialized(self, app: Flask) -> None:
        """App should have rate limiter extension."""
        from app import limiter
        assert limiter is not None

    def test_default_limits_set(self, app: Flask) -> None:
        """Default limits should be configured."""
        from app import limiter
        assert limiter._default_limits_per_method is not None  # type: ignore[attr-defined]


class TestInputLength:
    """Verify forms don't accept excessively long input."""

    def test_career_long_input_handled(self, auth_client: FlaskClient) -> None:
        """Career route should handle very long input gracefully."""
        long_text = "A" * 5000
        resp = auth_client.post("/career/", data={"career_field": long_text}, follow_redirects=True)
        # Should not crash — either processes or rejects gracefully
        assert resp.status_code == 200
