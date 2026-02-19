"""
Real-Time Job Market Trends Dashboard routes.
"""
from typing import List, Optional, Union
from flask import Blueprint, request, render_template, session, flash
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_trends_report
from app.services.dynamo_service import save_query

trends_bp = Blueprint("trends", __name__, url_prefix="/trends", template_folder="../templates")

INDUSTRIES: List[str] = [
    "Technology / IT", "Data Science & AI", "Cloud Computing",
    "Cybersecurity", "FinTech", "Healthcare Tech", "E-Commerce",
    "Digital Marketing", "Gaming", "Blockchain / Web3",
]


@trends_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard() -> Union[str, Response]:
    result: Optional[str] = None
    selected_industry: str = ""

    if request.method == "POST":
        selected_industry = request.form.get("industry", "").strip()
        if not selected_industry:
            flash("Please select or enter an industry.", "warning")
            return render_template("trends/dashboard.html", result=None,
                                   industries=INDUSTRIES, selected=selected_industry)
        try:
            result = generate_trends_report(selected_industry)
            save_query(
                user_id=session["user_id"],
                query_type="trends",
                input_text=f"Trends: {selected_industry}",
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("trends/dashboard.html", result=result,
                           industries=INDUSTRIES, selected=selected_industry)
