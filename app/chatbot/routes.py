"""
AI Career Chatbot — free-form multi-turn career conversation.
"""
from typing import Dict, List, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for, make_response
from werkzeug.wrappers import Response
import markdown as md  # type: ignore[import-untyped]

from app.auth.utils import login_required
from app.services.groq_service import chatbot_reply, CHATBOT_SYSTEM
from app.services.dynamo_service import save_query
from app.services.pdf_service import generate_pdf

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

    if not user_msg:
        flash("Please enter a message.", "warning")
        return redirect(url_for("chatbot.start"))

    if "chatbot_messages" not in session:
        return redirect(url_for("chatbot.start"))

    messages: List[Dict[str, str]] = session["chatbot_messages"]
    messages.append({"role": "user", "content": user_msg})

    try:
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


@chatbot_bp.route("/download-pdf")
@login_required
def download_pdf() -> Union[Response, tuple[str, int]]:
    """Export the current chat conversation as a styled PDF."""
    messages: List[Dict[str, str]] = session.get("chatbot_messages", [])
    if not messages:
        flash("No conversation to export.", "warning")
        return redirect(url_for("chatbot.start"))

    # Build HTML from chat messages (skip system prompt)
    html_parts: List[str] = []
    for msg in messages:
        if msg["role"] == "system":
            continue
        if msg["role"] == "user":
            html_parts.append(f'<p><strong style="color: #0d6efd;">You:</strong> {msg["content"]}</p>')
        else:
            converted: str = md.markdown(msg["content"], extensions=["tables", "fenced_code"])
            html_parts.append(f'<div style="background: #f0f4f8; padding: 10px; border-left: 4px solid #0d6efd; margin: 8px 0;">'
                              f'<strong>AI Career Expert:</strong>{converted}</div>')

    try:
        pdf_bytes: bytes = generate_pdf(
            title="AI Career Chatbot — Conversation Export",
            html_content="\n".join(html_parts),
            user_name=session.get("username", "User"),
        )
        response: Response = make_response(pdf_bytes)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=Career_Chatbot_Export.pdf"
        return response
    except Exception as exc:
        flash(f"PDF generation failed: {exc}", "danger")
        return redirect(url_for("chatbot.start"))
