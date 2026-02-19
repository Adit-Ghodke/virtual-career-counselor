"""
Skill Gap Heatmap — visual analysis of current vs required skills.
"""
import json
from typing import Any, Dict, Optional, Union
from flask import Blueprint, request, render_template, session, flash
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import analyze_skill_gap
from app.services.dynamo_service import save_query

skill_gap_bp = Blueprint("skill_gap", __name__, url_prefix="/skill-gap", template_folder="../templates")


@skill_gap_bp.route("/", methods=["GET", "POST"])
@login_required
def analyze() -> Union[str, Response]:
    result: Optional[Dict[str, Any]] = None
    chart_data: Optional[str] = None

    if request.method == "POST":
        current_skills = request.form.get("current_skills", "").strip()
        target_role = request.form.get("target_role", "").strip()
        experience = request.form.get("experience", "").strip()

        if not current_skills or not target_role:
            flash("Please provide your skills and target role.", "warning")
            return render_template("skill_gap/analyze.html", result=None, chart_data=None)

        raw: str = ""
        try:
            raw = analyze_skill_gap(current_skills, target_role, experience)

            # Parse JSON from AI response (may be wrapped in ```json``` blocks)
            cleaned: str = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            result = json.loads(cleaned)
            chart_data = json.dumps(result.get("skills", []) if result else [])

            save_query(
                user_id=session["user_id"],
                query_type="skill_gap",
                input_text=f"Skills: {current_skills} | Target: {target_role}",
                ai_response=raw,
            )
        except json.JSONDecodeError:
            # Fallback: show raw text if JSON parsing fails
            result = {"summary": raw, "skills": [], "readiness": 0, "priority_skills": [], "timeline": "N/A"}
            chart_data = "[]"
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("skill_gap/analyze.html", result=result, chart_data=chart_data)
