"""
Career Pivot Analyzer routes.
"""
from typing import Dict, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import analyze_career_pivot
from app.services.dynamo_service import save_query
from app.services.sns_service import send_report_email

pivot_bp = Blueprint("pivot", __name__, url_prefix="/pivot", template_folder="../templates")


@pivot_bp.route("/", methods=["GET", "POST"])
@login_required
def analyze() -> Union[str, Response]:
    result: Optional[str] = None
    form_data: Dict[str, str] = {}

    if request.method == "POST":
        current_role = request.form.get("current_role", "").strip()
        years_exp = request.form.get("years_exp", "").strip()
        target_role = request.form.get("target_role", "").strip()
        current_skills = request.form.get("current_skills", "").strip()
        form_data = {
            "current_role": current_role, "years_exp": years_exp,
            "target_role": target_role, "current_skills": current_skills,
        }

        if not current_role or not target_role:
            flash("Current role and target role are required.", "warning")
            return render_template("pivot/analyzer.html", result=None, form_data=form_data)

        try:
            result = analyze_career_pivot(current_role, years_exp or "0", target_role, current_skills or "Not specified")
            save_query(
                user_id=session["user_id"],
                query_type="pivot",
                input_text=f"{current_role} → {target_role}",
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("pivot/analyzer.html", result=result, form_data=form_data)


@pivot_bp.route("/email", methods=["POST"])
@login_required
def email_report() -> Response:
    report_body: str = request.form.get("report_body", "") or ""
    if report_body:
        send_report_email(session.get("user_name", "User"), "Career Pivot Analysis", report_body)
        flash("Pivot analysis emailed!", "success")
    return redirect(url_for("pivot.analyze"))
