"""
Cover Letter Generator — AI-powered tailored cover letters.
"""
from typing import Optional, Union
from flask import Blueprint, request, render_template, session, flash
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import generate_cover_letter
from app.services.dynamo_service import save_query
from app.services.resume_parser import parse_resume

cover_letter_bp = Blueprint("cover_letter", __name__, url_prefix="/cover-letter", template_folder="../templates")


@cover_letter_bp.route("/", methods=["GET", "POST"])
@login_required
def generate() -> Union[str, Response]:
    result: Optional[str] = None

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        job_description = request.form.get("job_description", "").strip()
        company_name = request.form.get("company_name", "").strip()

        # Handle PDF/DOCX upload — extract text and merge with pasted text
        resume_file = request.files.get("resume_file")
        if resume_file and resume_file.filename:
            try:
                extracted: str = parse_resume(resume_file, resume_file.filename)
                resume_text = f"{extracted}\n\n{resume_text}".strip() if resume_text else extracted
            except ValueError as ve:
                flash(str(ve), "warning")
                return render_template("cover_letter/generate.html", result=None)
            except Exception:
                flash("Could not read the uploaded file. Please paste your resume instead.", "warning")
                return render_template("cover_letter/generate.html", result=None)

        if not job_description or not company_name:
            flash("Please provide at least the job description and company name.", "warning")
            return render_template("cover_letter/generate.html", result=None)

        try:
            result = generate_cover_letter(resume_text, job_description, company_name)
            save_query(
                user_id=session["user_id"],
                query_type="cover_letter",
                input_text=f"Company: {company_name}\n{job_description[:500]}",
                ai_response=result,
            )
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("cover_letter/generate.html", result=result)
