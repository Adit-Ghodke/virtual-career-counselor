"""
Resume Analysis & Job Matching routes.
"""
from typing import Optional, Set, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import analyze_resume
from app.services.dynamo_service import save_query, award_badge
from app.services.resume_parser import parse_resume
from app.services.sns_service import send_report_email

resume_bp = Blueprint("resume", __name__, url_prefix="/resume", template_folder="../templates")

UPLOAD_EXTENSIONS: Set[str] = {"pdf", "docx", "doc"}


@resume_bp.route("/", methods=["GET", "POST"])
@login_required
def upload() -> Union[str, Response]:
    result: Optional[str] = None
    target_role: str = ""

    if request.method == "POST":
        target_role = request.form.get("target_role", "").strip()
        file = request.files.get("resume_file")

        if not file or not file.filename:
            flash("Please upload a resume file (PDF or DOCX).", "warning")
            return render_template("resume/upload.html", result=None, target_role=target_role)

        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in UPLOAD_EXTENSIONS:
            flash("Only PDF and DOCX files are supported.", "danger")
            return render_template("resume/upload.html", result=None, target_role=target_role)

        if not target_role:
            flash("Please enter your target job role.", "warning")
            return render_template("resume/upload.html", result=None, target_role=target_role)

        try:
            resume_text = parse_resume(file, file.filename)
            if len(resume_text.strip()) < 50:
                flash("Could not extract enough text from the resume. Try a different file.", "warning")
                return render_template("resume/upload.html", result=None, target_role=target_role)

            result = analyze_resume(resume_text, target_role)
            save_query(
                user_id=session["user_id"],
                query_type="resume",
                input_text=f"Resume analysis for: {target_role}",
                ai_response=result,
            )
            # Badge: first resume upload
            award_badge(session["user_id"], "Resume Uploaded", "bi-file-earmark-person", "Uploaded your first resume for AI analysis")

        except Exception as exc:
            flash(f"Error: {exc}", "danger")

    return render_template("resume/upload.html", result=result, target_role=target_role)


@resume_bp.route("/email", methods=["POST"])
@login_required
def email_report() -> Response:
    report_body: str = request.form.get("report_body", "") or ""
    if report_body:
        send_report_email(session.get("user_name", "User"), "Resume Analysis", report_body)
        flash("Resume analysis report emailed!", "success")
    return redirect(url_for("resume.upload"))
