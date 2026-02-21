"""
Shared pytest fixtures for Virtual Career Counselor tests.
"""
import os
import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture(scope="session", autouse=True)
def _set_env() -> None:  # pyright: ignore[reportUnusedFunction]
    """Set required environment variables before app creation."""
    os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
    os.environ.setdefault("FLASK_ENV", "development")
    os.environ.setdefault("GROQ_API_KEY", "test-groq-key")
    os.environ.setdefault("AWS_REGION", "us-east-1")
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
    os.environ.setdefault("TAVILY_API_KEY", "test-tavily-key")


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    """Create a fresh Flask app for each test."""
    from app import create_app
    test_app: Flask = create_app()
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    yield test_app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """Flask test client."""
    return app.test_client()


@pytest.fixture()
def auth_client(client: FlaskClient, app: Flask) -> FlaskClient:
    """Authenticated test client (logged-in user session)."""
    with client.session_transaction() as sess:
        sess["user_id"] = "test-user-123"
        sess["user_name"] = "Test User"
        sess["email"] = "test@example.com"
        sess["role"] = "user"
    return client


@pytest.fixture()
def admin_client(client: FlaskClient, app: Flask) -> FlaskClient:
    """Admin-authenticated test client."""
    with client.session_transaction() as sess:
        sess["user_id"] = "admin-user-456"
        sess["user_name"] = "Admin User"
        sess["email"] = "admin@example.com"
        sess["role"] = "admin"
    return client


# ── Mock external services ──────────────────────────────────────

@pytest.fixture(autouse=True)
def mock_dynamo() -> Generator[MagicMock, None, None]:
    """Mock all DynamoDB operations to avoid real AWS calls."""
    with patch("app.services.dynamo_service.boto3") as mock_boto:
        mock_table = MagicMock()
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = {}
        mock_table.query.return_value = {"Items": [], "Count": 0}
        mock_table.scan.return_value = {"Items": [], "Count": 0}
        mock_boto.resource.return_value.Table.return_value = mock_table
        yield mock_boto


@pytest.fixture(autouse=True)
def mock_groq() -> Generator[MagicMock, None, None]:
    """Mock Groq API client to avoid real API calls."""
    with patch("app.services.groq_service._get_client") as mock_client_fn:
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "This is a mock AI response for testing."
        mock_client.chat.completions.create.return_value = mock_completion
        mock_client_fn.return_value = mock_client
        yield mock_client


@pytest.fixture(autouse=True)
def mock_tavily() -> Generator[MagicMock, None, None]:
    """Mock Tavily web search to avoid real API calls."""
    with patch("app.services.web_search_service._get_tavily_client") as mock_fn:
        mock_tavily_client = MagicMock()
        mock_tavily_client.search.return_value = {
            "results": [
                {"title": "Test Result", "url": "https://example.com", "content": "Mock search content."}
            ],
            "answer": "Mock Tavily answer.",
        }
        mock_fn.return_value = mock_tavily_client
        yield mock_tavily_client


@pytest.fixture(autouse=True)
def mock_sns() -> Generator[MagicMock, None, None]:
    """Mock SNS to avoid real email sends."""
    with patch("app.services.sns_service.boto3") as mock_boto:
        mock_boto.client.return_value.publish.return_value = {"MessageId": "test-msg-id"}
        yield mock_boto
