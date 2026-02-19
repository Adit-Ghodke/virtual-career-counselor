"""
Weekly AI Career Digest — preferences & on-demand generation.
"""
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_weekly_digest
from app.services.dynamo_service import save_digest_prefs, get_digest_prefs, save_query

digest_bp = Blueprint("digest", __name__, url_prefix="/digest", template_folder="../templates")

INDUSTRY_OPTIONS: List[str] = [
    "Technology", "Healthcare", "Finance", "Education", "Marketing",
    "Design", "Data Science", "Cybersecurity", "E-Commerce", "Manufacturing",
    "Consulting", "Media & Entertainment", "Legal", "Real Estate", "AI/ML",
]


@digest_bp.route("/", methods=["GET", "POST"])
@login_required
def preferences() -> Union[str, Response]:
    """Set weekly digest preferences."""
    user_id: str = session["user_id"]
    try:
        prefs: Optional[Dict[str, Any]] = get_digest_prefs(user_id)
    except Exception:
        prefs = None

    if request.method == "POST":
        selected: List[str] = request.form.getlist("industries")
        enabled: bool = request.form.get("enabled") == "on"

        try:
            save_digest_prefs(user_id, selected, enabled)
            flash("Digest preferences saved!", "success")
            prefs = {"industries": selected, "enabled": enabled}
        except Exception as exc:
            flash(f"Error: {exc}", "danger")

    return render_template(
        "digest/preferences.html",
        prefs=prefs,
        industry_options=INDUSTRY_OPTIONS,
    )


@digest_bp.route("/generate", methods=["POST"])
@login_required
def generate() -> Union[str, Response]:
    """Generate an on-demand digest now."""
    user_id: str = session["user_id"]
    try:
        prefs: Optional[Dict[str, Any]] = get_digest_prefs(user_id)
    except Exception:
        prefs = None
    industries: List[str] = prefs.get("industries", ["Technology"]) if prefs else ["Technology"]

    try:
        result = generate_weekly_digest(industries)
        save_query(user_id=user_id, query_type="weekly_digest", input_text=", ".join(industries), ai_response=result)
        return render_template("digest/result.html", result=result, industries=industries)
    except Exception as exc:
        flash(f"Error generating digest: {exc}", "danger")
        return redirect(url_for("digest.preferences"))
