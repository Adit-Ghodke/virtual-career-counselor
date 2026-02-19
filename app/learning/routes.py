"""
Personalized Learning Path with Progress Tracking routes.
"""
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_learning_path
from app.services.dynamo_service import (
    save_query, save_user_progress, get_user_progress,
    update_progress_weeks, award_badge,
)

learning_bp = Blueprint("learning", __name__, url_prefix="/learning", template_folder="../templates")


@learning_bp.route("/", methods=["GET", "POST"])
@login_required
def roadmap() -> Union[str, Response]:
    result: Optional[str] = None
    form_data: Dict[str, str] = {}

    if request.method == "POST":
        target_role = request.form.get("target_role", "").strip()
        current_skills = request.form.get("current_skills", "").strip()
        hours_per_day = request.form.get("hours_per_day", "2").strip()
        form_data = {"target_role": target_role, "current_skills": current_skills, "hours_per_day": hours_per_day}

        if not target_role:
            flash("Please enter a target role.", "warning")
            return render_template("learning/roadmap.html", result=None, form_data=form_data, progress_list=[])

        try:
            result = generate_learning_path(target_role, current_skills or "None specified", hours_per_day)
            save_query(
                user_id=session["user_id"],
                query_type="learning_path",
                input_text=f"Learning path for {target_role}",
                ai_response=result,
            )
            # Count weeks in result (heuristic)
            week_count = result.lower().count("### week")
            if week_count < 4:
                week_count = 8
            save_user_progress(session["user_id"], "", target_role, week_count, [])

        except Exception as exc:
            flash(f"Error: {exc}", "danger")

    progress_list: List[Dict[str, Any]] = get_user_progress(session.get("user_id", ""))
    return render_template("learning/roadmap.html", result=result, form_data=form_data, progress_list=progress_list)


@learning_bp.route("/update-progress", methods=["POST"])
@login_required
def update_progress() -> Response:
    progress_id: str = request.form.get("progress_id", "") or ""
    completed: List[str] = request.form.getlist("completed_weeks")
    completed_ints: List[int] = [int(w) for w in completed if w.isdigit()]

    if progress_id:
        update_progress_weeks(progress_id, session["user_id"], completed_ints)
        if len(completed_ints) >= 4:
            award_badge(session["user_id"], "Consistent Learner", "bi-journal-check", "Completed 4+ weeks in a learning path")
        flash("Progress updated!", "success")

    return redirect(url_for("learning.roadmap"))
