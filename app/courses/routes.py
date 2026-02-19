"""
Course Recommendation routes.
"""
from typing import Dict, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_course_recommendations
from app.services.dynamo_service import save_query
from app.services.sns_service import send_report_email

courses_bp = Blueprint("courses", __name__, url_prefix="/courses", template_folder="../templates")


@courses_bp.route("/", methods=["GET", "POST"])
@login_required
def recommend() -> Union[str, Response]:
    result: Optional[str] = None
    form_data: Dict[str, str] = {}

    if request.method == "POST":
        interests: str = request.form.get("interests", "").strip()
        skill_level: str = request.form.get("skill_level", "").strip()
        learning_goals: str = request.form.get("learning_goals", "").strip()
        time_availability: str = request.form.get("time_availability", "").strip()
        form_data = {
            "interests": interests,
            "skill_level": skill_level,
            "learning_goals": learning_goals,
            "time_availability": time_availability,
        }

        if not interests or not learning_goals:
            flash("Interests and learning goals are required.", "warning")
            return render_template("courses/course_result.html", result=None, form_data=form_data)

        try:
            result = generate_course_recommendations(
                interests=interests,
                skill_level=skill_level or "Beginner",
                learning_goals=learning_goals,
                time_availability=time_availability or "5",
            )
            input_summary = f"Interests: {interests} | Level: {skill_level} | Goals: {learning_goals}"
            save_query(
                user_id=session["user_id"],
                query_type="course",
                input_text=input_summary,
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI service error: {exc}", "danger")

    return render_template("courses/course_result.html", result=result, form_data=form_data)


@courses_bp.route("/email", methods=["POST"])
@login_required
def email_report() -> Response:
    report_body: str = request.form.get("report_body", "") or ""
    if report_body:
        send_report_email(
            user_name=session.get("user_name", "User"),
            report_type="Course Recommendations",
            report_body=report_body,
        )
        flash("Course report emailed successfully!", "success")
    else:
        flash("No report to send.", "warning")
    return redirect(url_for("courses.recommend"))
