"""
Career Path Exploration routes.
"""
from typing import Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_career_overview
from app.services.dynamo_service import save_query
from app.services.sns_service import send_report_email

career_bp = Blueprint("career", __name__, url_prefix="/career", template_folder="../templates")


@career_bp.route("/", methods=["GET", "POST"])
@login_required
def explore() -> Union[str, Response]:
    result: Optional[str] = None
    career_name: str = ""

    if request.method == "POST":
        career_name = request.form.get("career_name", "").strip()

        if not career_name or len(career_name) > 300:
            flash("Please enter a valid career name (max 300 characters).", "warning")
            return render_template("career/career_result.html", result=None, career_name=career_name)

        try:
            result = generate_career_overview(career_name)
            # Persist to DynamoDB
            save_query(
                user_id=session["user_id"],
                query_type="career",
                input_text=career_name,
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI service error: {exc}", "danger")

    return render_template("career/career_result.html", result=result, career_name=career_name)


@career_bp.route("/email", methods=["POST"])
@login_required
def email_report() -> Response:
    """Send the last career result to the user via SNS."""
    report_body: str = request.form.get("report_body", "") or ""
    if report_body:
        send_report_email(
            user_name=session.get("user_name", "User"),
            report_type="Career Path",
            report_body=report_body,
        )
        flash("Career report emailed successfully!", "success")
    else:
        flash("No report to send.", "warning")
    return redirect(url_for("career.explore"))
