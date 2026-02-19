"""
Job Market Insights routes.
"""
from typing import Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_market_insights
from app.services.dynamo_service import save_query
from app.services.sns_service import send_report_email

insights_bp = Blueprint("insights", __name__, url_prefix="/insights", template_folder="../templates")


@insights_bp.route("/", methods=["GET", "POST"])
@login_required
def market() -> Union[str, Response]:
    result: Optional[str] = None
    role_name: str = ""

    if request.method == "POST":
        role_name = request.form.get("role_name", "").strip()

        if not role_name or len(role_name) > 300:
            flash("Please enter a valid job role or industry (max 300 chars).", "warning")
            return render_template("insights/insights_result.html", result=None, role_name=role_name)

        try:
            result = generate_market_insights(role_name)
            save_query(
                user_id=session["user_id"],
                query_type="insights",
                input_text=role_name,
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI service error: {exc}", "danger")

    return render_template("insights/insights_result.html", result=result, role_name=role_name)


@insights_bp.route("/email", methods=["POST"])
@login_required
def email_report() -> Response:
    report_body: str = request.form.get("report_body", "") or ""
    if report_body:
        send_report_email(
            user_name=session.get("user_name", "User"),
            report_type="Job Market Insights",
            report_body=report_body,
        )
        flash("Insights report emailed successfully!", "success")
    else:
        flash("No report to send.", "warning")
    return redirect(url_for("insights.market"))
