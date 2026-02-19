"""
AI Mentor Chat — persistent career mentor with memory.
"""
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import mentor_reply, MENTOR_SYSTEM
from app.services.dynamo_service import save_mentor_chat, get_mentor_chat, save_query

mentor_bp = Blueprint("mentor", __name__, url_prefix="/mentor", template_folder="../templates")


@mentor_bp.route("/", methods=["GET", "POST"])
@login_required
def chat() -> Union[str, Response]:
    """Initialize or continue mentor chat."""
    user_id: str = session["user_id"]

    # Load persistent chat from DynamoDB
    try:
        saved: Optional[Dict[str, Any]] = get_mentor_chat(user_id)
    except Exception:
        saved = None

    if saved and "mentor_messages" not in session:
        session["mentor_messages"] = saved.get("messages", [])
        session["mentor_goals"] = saved.get("goals", "")

    if "mentor_messages" not in session:
        session["mentor_messages"] = [
            {"role": "system", "content": MENTOR_SYSTEM},
            {"role": "assistant", "content": "Hello! I'm your dedicated career mentor. 🌟\n\nBefore we begin, tell me a bit about yourself:\n- What's your current role/field?\n- Where do you want to be in 2-3 years?\n- What's your biggest career challenge right now?\n\nI'm here to guide you every step of the way!"},
        ]
        session["mentor_goals"] = ""

    if request.method == "POST":
        action = request.form.get("action", "send")

        if action == "set_goals":
            goals: str = request.form.get("goals", "").strip()
            session["mentor_goals"] = goals
            # Inject goals into the conversation
            msgs: List[Dict[str, str]] = session["mentor_messages"]
            msgs.append({"role": "user", "content": f"My career goals: {goals}"})
            try:
                reply = mentor_reply(msgs)
                msgs.append({"role": "assistant", "content": reply})
                session["mentor_messages"] = msgs
                # Persist to DynamoDB (may fail if table not created yet)
                try:
                    save_mentor_chat(user_id, msgs, goals)
                except Exception:
                    pass
            except Exception as exc:
                flash(f"AI error: {exc}", "danger")
            return redirect(url_for("mentor.chat"))

        elif action == "send":
            user_msg = request.form.get("message", "").strip()
            if not user_msg:
                flash("Please enter a message.", "warning")
                return redirect(url_for("mentor.chat"))

            msgs = session["mentor_messages"]
            msgs.append({"role": "user", "content": user_msg})
            try:
                reply = mentor_reply(msgs)
                msgs.append({"role": "assistant", "content": reply})
                session["mentor_messages"] = msgs
                try:
                    save_mentor_chat(user_id, msgs, session.get("mentor_goals", ""))
                except Exception:
                    pass
                save_query(user_id=user_id, query_type="mentor", input_text=user_msg, ai_response=reply)
            except Exception as exc:
                flash(f"AI error: {exc}", "danger")
            return redirect(url_for("mentor.chat"))

    return render_template("mentor/chat.html", goals=session.get("mentor_goals", ""))


@mentor_bp.route("/clear", methods=["POST"])
@login_required
def clear() -> Response:
    """Reset mentor conversation."""
    session.pop("mentor_messages", None)
    session.pop("mentor_goals", None)
    flash("Mentor conversation reset.", "info")
    return redirect(url_for("mentor.chat"))
