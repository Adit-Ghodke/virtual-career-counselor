"""
AI Career Chatbot — free-form multi-turn career conversation.
"""
from typing import Dict, List, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import chatbot_reply, CHATBOT_SYSTEM, rag_enhanced_query
from app.services.rag_service import get_rag_context
from app.services.dynamo_service import save_query

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot", template_folder="../templates")


@chatbot_bp.route("/")
@login_required
def start() -> Union[str, Response]:
    """Initialize or continue the chatbot session."""
    if "chatbot_messages" not in session:
        session["chatbot_messages"] = [
            {"role": "system", "content": CHATBOT_SYSTEM},
            {"role": "assistant", "content": "Hi! I'm your AI career counselor. 🎓 Ask me anything about careers, job search, skills, salary negotiation, interview tips, or career transitions. How can I help you today?"},
        ]
    return render_template("chatbot/chat.html")


@chatbot_bp.route("/send", methods=["POST"])
@login_required
def send() -> Union[str, Response]:
    """Handle a user message and return AI reply."""
    user_msg: str = request.form.get("message", "").strip()
    use_rag: bool = request.form.get("use_rag") == "on"

    if not user_msg:
        flash("Please enter a message.", "warning")
        return redirect(url_for("chatbot.start"))

    if "chatbot_messages" not in session:
        return redirect(url_for("chatbot.start"))

    messages: List[Dict[str, str]] = session["chatbot_messages"]
    messages.append({"role": "user", "content": user_msg})

    try:
        if use_rag:
            rag_ctx = get_rag_context(user_msg, n_results=3)
            reply = rag_enhanced_query(user_msg, rag_ctx)
        else:
            reply = chatbot_reply(messages)

        messages.append({"role": "assistant", "content": reply})
        session["chatbot_messages"] = messages

        # Save to query history
        save_query(
            user_id=session["user_id"],
            query_type="chatbot",
            input_text=user_msg,
            ai_response=reply,
        )
    except Exception as exc:
        flash(f"AI error: {exc}", "danger")

    return redirect(url_for("chatbot.start"))


@chatbot_bp.route("/clear", methods=["POST"])
@login_required
def clear() -> Response:
    """Reset the chatbot conversation."""
    session.pop("chatbot_messages", None)
    flash("Conversation cleared.", "info")
    return redirect(url_for("chatbot.start"))
