"""
Peer Comparison / Anonymous Benchmarking routes.
"""
from typing import Dict, Optional, Union
from flask import Blueprint, request, render_template, session, flash
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_peer_comparison
from app.services.dynamo_service import save_query, award_badge

peers_bp = Blueprint("peers", __name__, url_prefix="/peers", template_folder="../templates")


@peers_bp.route("/", methods=["GET", "POST"])
@login_required
def compare() -> Union[str, Response]:
    result: Optional[str] = None
    form_data: Dict[str, str] = {}

    if request.method == "POST":
        target_role = request.form.get("target_role", "").strip()
        skills = request.form.get("skills", "").strip()
        experience = request.form.get("experience", "").strip()
        form_data = {"target_role": target_role, "skills": skills, "experience": experience}

        if not target_role or not skills:
            flash("Target role and skills are required.", "warning")
            return render_template("peers/comparison.html", result=None, form_data=form_data)

        try:
            result = generate_peer_comparison(target_role, skills, experience or "Fresher")
            save_query(
                user_id=session["user_id"],
                query_type="peer_compare",
                input_text=f"Peer compare for {target_role}",
                ai_response=result,
            )
            award_badge(session["user_id"], "Benchmarker", "bi-bar-chart-steps", "Completed a peer comparison analysis")
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("peers/comparison.html", result=result, form_data=form_data)
