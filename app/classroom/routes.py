"""
Team/Classroom Mode — share AI results and collaborate.
"""
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.dynamo_service import (
    create_classroom, get_classroom_by_code, get_classroom,
    join_classroom, get_user_classrooms, get_user_queries,
)

classroom_bp = Blueprint("classroom", __name__, url_prefix="/classroom", template_folder="../templates")


@classroom_bp.route("/")
@login_required
def index() -> Union[str, Response]:
    """List user's classrooms."""
    try:
        classrooms: List[Dict[str, Any]] = get_user_classrooms(session["user_id"])
    except Exception:
        classrooms = []
    return render_template("classroom/index.html", classrooms=classrooms)


@classroom_bp.route("/create", methods=["POST"])
@login_required
def create() -> Response:
    """Create a new classroom."""
    name: str = request.form.get("name", "").strip()
    if not name:
        flash("Please enter a classroom name.", "warning")
        return redirect(url_for("classroom.index"))

    try:
        room: Dict[str, Any] = create_classroom(name, session["user_id"], session.get("user_name", "User"))
        flash(f"Classroom '{name}' created! Share code: {room['join_code']}", "success")
    except Exception as exc:
        flash(f"Error: {exc}", "danger")

    return redirect(url_for("classroom.index"))


@classroom_bp.route("/join", methods=["POST"])
@login_required
def join() -> Response:
    """Join a classroom by code."""
    code: str = request.form.get("code", "").strip()
    if not code:
        flash("Please enter a join code.", "warning")
        return redirect(url_for("classroom.index"))

    try:
        room: Optional[Dict[str, Any]] = get_classroom_by_code(code)
    except Exception:
        room = None
    if not room:
        flash("Invalid join code.", "danger")
        return redirect(url_for("classroom.index"))

    success: bool = join_classroom(room["classroom_id"], session["user_id"], session.get("user_name", "User"))
    if success:
        flash(f"Joined classroom '{room['name']}'!", "success")
    else:
        flash("Could not join classroom.", "danger")

    return redirect(url_for("classroom.index"))


@classroom_bp.route("/<classroom_id>")
@login_required
def view(classroom_id: str) -> Union[str, Response]:
    """View classroom details and member activity."""
    try:
        room = get_classroom(classroom_id)
    except Exception:
        room = None
    if not room:
        flash("Classroom not found.", "warning")
        return redirect(url_for("classroom.index"))

    # Check membership
    members = room.get("members", [])
    if not any(m["user_id"] == session["user_id"] for m in members):
        flash("You are not a member of this classroom.", "danger")
        return redirect(url_for("classroom.index"))

    # Gather member activity summary
    member_activity: List[Dict[str, Any]] = []
    for m in members:
        queries: List[Dict[str, Any]] = get_user_queries(m["user_id"], limit=10)
        member_activity.append({
            "name": m["name"],
            "role": m["role"],
            "recent_queries": len(queries),
            "last_active": queries[0].get("created_at", "N/A")[:10] if queries else "Never",
        })

    return render_template("classroom/view.html", room=room, member_activity=member_activity)
