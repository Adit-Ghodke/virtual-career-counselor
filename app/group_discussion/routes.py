"""
Mock Group Discussion — AI simulates panelists for GD practice.
"""
from typing import Dict, List, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import group_discussion_reply, GD_SYSTEM
from app.services.dynamo_service import save_query

gd_bp = Blueprint("group_discussion", __name__, url_prefix="/gd", template_folder="../templates")


@gd_bp.route("/", methods=["GET", "POST"])
@login_required
def start() -> Union[str, Response]:
    """Select a GD topic and begin."""
    if request.method == "POST":
        topic: str = request.form.get("topic", "").strip()
        custom_topic: str = request.form.get("custom_topic", "").strip()
        topic = custom_topic if custom_topic else topic

        if not topic:
            flash("Please select or enter a topic.", "warning")
            return render_template("group_discussion/start.html")

        session["gd_topic"] = topic
        session["gd_round"] = 1
        system_msg: str = GD_SYSTEM + f"\n\nThe GD topic is: **{topic}**"
        session["gd_messages"] = [
            {"role": "system", "content": system_msg},
            {"role": "assistant", "content": f"**Moderator:** Welcome to this Group Discussion! Today's topic is: **\"{topic}\"**\n\nLet me introduce our panelists:\n- **Panelist A** — will focus on the pros\n- **Panelist B** — will play devil's advocate\n- **Panelist C** — will bring real-world examples\n\nYou are a participant. Please share your opening thoughts on this topic. You have about 2 minutes. Go ahead!"},
        ]
        return redirect(url_for("group_discussion.discuss"))

    return render_template("group_discussion/start.html")


@gd_bp.route("/discuss", methods=["GET", "POST"])
@login_required
def discuss() -> Union[str, Response]:
    """Continue the GD conversation."""
    if "gd_messages" not in session:
        return redirect(url_for("group_discussion.start"))

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if not user_msg:
            flash("Please share your thoughts.", "warning")
            return redirect(url_for("group_discussion.discuss"))

        messages: List[Dict[str, str]] = session["gd_messages"]
        round_num: int = session.get("gd_round", 1)

        # Add round context
        if round_num >= 5:
            user_msg += "\n\n[This is round 5+. Please provide the final evaluation and verdict after responding.]"

        messages.append({"role": "user", "content": user_msg})

        try:
            reply = group_discussion_reply(messages)
            messages.append({"role": "assistant", "content": reply})
            session["gd_messages"] = messages
            session["gd_round"] = round_num + 1

            save_query(
                user_id=session["user_id"],
                query_type="group_discussion",
                input_text=f"GD Topic: {session.get('gd_topic', '')} | Round {round_num}",
                ai_response=reply,
            )
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

        return redirect(url_for("group_discussion.discuss"))

    return render_template(
        "group_discussion/discuss.html",
        topic=session.get("gd_topic", ""),
        round_num=session.get("gd_round", 1),
    )


@gd_bp.route("/reset", methods=["POST"])
@login_required
def reset() -> Response:
    """Reset the GD session."""
    session.pop("gd_messages", None)
    session.pop("gd_topic", None)
    session.pop("gd_round", None)
    flash("Group Discussion reset.", "info")
    return redirect(url_for("group_discussion.start"))
