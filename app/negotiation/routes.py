"""
Salary Negotiation Simulator — multi-turn AI conversation.
"""
import json
from typing import Dict, List, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import negotiation_reply, NEGOTIATION_SYSTEM
from app.services.dynamo_service import save_conversation, award_badge

negotiation_bp = Blueprint("negotiation", __name__, url_prefix="/negotiation", template_folder="../templates")


@negotiation_bp.route("/", methods=["GET"])
@login_required
def start() -> Union[str, Response]:
    """Show the negotiation setup form."""
    return render_template("negotiation/simulator.html", chat=None, setup=True, round_num=0)


@negotiation_bp.route("/begin", methods=["POST"])
@login_required
def begin() -> Union[str, Response]:
    """Start a new negotiation session."""
    role: str = request.form.get("role", "").strip()
    company_type: str = request.form.get("company_type", "").strip()
    experience: str = request.form.get("experience", "").strip()
    expected_salary: str = request.form.get("expected_salary", "").strip()

    if not role or not experience or not expected_salary:
        flash("Please fill in all fields.", "warning")
        return redirect(url_for("negotiation.start"))

    system_msg: Dict[str, str] = {
        "role": "system",
        "content": NEGOTIATION_SYSTEM,
    }
    user_setup: Dict[str, str] = {
        "role": "user",
        "content": (
            f"I'm negotiating for a {role} position at a {company_type}.\n"
            f"My expected salary: {expected_salary}\n"
            f"Years of experience: {experience}\n\n"
            "Start the negotiation. You are the HR manager — begin by acknowledging "
            "my profile and push back on my salary expectations."
        ),
    }

    messages: List[Dict[str, str]] = [system_msg, user_setup]
    try:
        ai_response: str = negotiation_reply(messages)
        messages.append({"role": "assistant", "content": ai_response})
    except Exception as exc:
        flash(f"AI error: {exc}", "danger")
        return redirect(url_for("negotiation.start"))

    # Store in session for multi-turn
    session["neg_messages"] = json.dumps(messages)
    session["neg_round"] = 1
    session["neg_meta"] = json.dumps({"role": role, "company_type": company_type, "salary": expected_salary})

    chat_display: List[Dict[str, str]] = _build_chat_display(messages)
    return render_template("negotiation/simulator.html", conversation=chat_display,
                           round=1, finished=False)


@negotiation_bp.route("/reply", methods=["POST"])
@login_required
def reply() -> Union[str, Response]:
    """Handle user's negotiation reply."""
    user_input: str = request.form.get("user_reply", "").strip()
    if not user_input:
        flash("Please type your negotiation response.", "warning")
        return redirect(url_for("negotiation.start"))

    messages: List[Dict[str, str]] = json.loads(session.get("neg_messages", "[]"))
    round_num: int = session.get("neg_round", 1)

    if not messages:
        flash("Session expired. Please start a new negotiation.", "warning")
        return redirect(url_for("negotiation.start"))

    messages.append({"role": "user", "content": user_input})

    # If this is round 4+, ask AI to wrap up
    if round_num >= 4:
        messages.append({
            "role": "user",
            "content": "(This is the final round. Please provide the final negotiation summary, scores, and recommendations.)"
        })

    try:
        ai_response = negotiation_reply(messages)
        messages.append({"role": "assistant", "content": ai_response})
    except Exception as exc:
        flash(f"AI error: {exc}", "danger")
        return redirect(url_for("negotiation.start"))

    round_num += 1
    session["neg_messages"] = json.dumps(messages)
    session["neg_round"] = round_num

    # Save completed negotiation
    if round_num > 4:
        save_conversation(session["user_id"], "negotiation", messages)
        award_badge(session["user_id"], "Negotiator", "bi-cash-coin", "Completed a salary negotiation simulation")
        session.pop("neg_messages", None)
        session.pop("neg_round", None)

    chat_display: List[Dict[str, str]] = _build_chat_display(messages)
    finished: bool = round_num > 4
    return render_template("negotiation/simulator.html", conversation=chat_display,
                           round=round_num, finished=finished)


def _build_chat_display(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Convert raw messages to display-friendly format (skip system)."""
    return [m for m in messages if m["role"] != "system"]
