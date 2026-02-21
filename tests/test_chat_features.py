"""
Tests for AI chat features — Chatbot, Mentor, Group Discussion.
"""
from flask.testing import FlaskClient
from unittest.mock import patch


class TestChatbotRoutes:
    """Test chatbot blueprint."""

    def test_chatbot_start_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/chatbot/")
        assert resp.status_code == 200

    @patch("app.chatbot.routes.chatbot_reply", return_value="Mock chatbot reply")
    @patch("app.chatbot.routes.save_query")
    def test_chatbot_send(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/chatbot/send", data={"message": "What career suits me?"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_chatbot_clear(self, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/chatbot/clear", follow_redirects=True)
        assert resp.status_code == 200

    def test_chatbot_unauthenticated_redirects(self, client: FlaskClient) -> None:
        resp = client.get("/chatbot/")
        assert resp.status_code in (302, 303)


class TestMentorRoutes:
    """Test mentor blueprint."""

    def test_mentor_get_renders(self, auth_client: FlaskClient) -> None:
        with patch("app.mentor.routes.get_mentor_chat", return_value=None):
            resp = auth_client.get("/mentor/")
            assert resp.status_code == 200

    @patch("app.mentor.routes.mentor_reply", return_value="Mock mentor reply")
    @patch("app.mentor.routes.save_mentor_chat")
    @patch("app.mentor.routes.get_mentor_chat", return_value=None)
    @patch("app.mentor.routes.save_query")
    def test_mentor_post(self, mock_sq: object, mock_get: object, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/mentor/", data={"message": "Help me plan", "goal": "SWE"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_mentor_clear(self, auth_client: FlaskClient) -> None:
        with patch("app.mentor.routes.save_mentor_chat"):
            resp = auth_client.post("/mentor/clear", follow_redirects=True)
            assert resp.status_code == 200


class TestGroupDiscussionRoutes:
    """Test group discussion blueprint."""

    def test_gd_start_renders(self, auth_client: FlaskClient) -> None:
        resp = auth_client.get("/gd/")
        assert resp.status_code == 200

    @patch("app.group_discussion.routes.group_discussion_reply", return_value="Mock GD reply")
    @patch("app.group_discussion.routes.save_query")
    def test_gd_discuss(self, mock_save: object, mock_ai: object, auth_client: FlaskClient) -> None:
        # First start a topic
        with auth_client.session_transaction() as sess:
            sess["gd_history"] = [
                {"role": "system", "content": "GD system prompt"},
                {"role": "assistant", "content": "Welcome to the discussion."},
            ]
            sess["gd_topic"] = "AI Ethics"
            sess["gd_round"] = 1
        resp = auth_client.post("/gd/discuss", data={"message": "I think AI is great"}, follow_redirects=True)
        assert resp.status_code == 200

    def test_gd_reset(self, auth_client: FlaskClient) -> None:
        resp = auth_client.post("/gd/reset", follow_redirects=True)
        assert resp.status_code == 200
