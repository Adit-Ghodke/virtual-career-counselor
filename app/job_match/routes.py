"""
Smart Career Search — Tavily AI web search + Groq analysis for real-time career intelligence.
"""
from typing import Dict, List, Optional, Union
from flask import Blueprint, request, render_template, session, flash, make_response, redirect, url_for
from werkzeug.wrappers import Response
import markdown as md  # type: ignore[import-untyped]

from app.auth.utils import login_required
from app.services.groq_service import smart_career_search
from app.services.dynamo_service import save_query
from app.services.pdf_service import generate_pdf

job_match_bp = Blueprint("job_match", __name__, url_prefix="/job-match", template_folder="../templates")


@job_match_bp.route("/", methods=["GET", "POST"])
@login_required
def match() -> Union[str, Response]:
    """Tavily-powered career search with Groq AI synthesis."""
    result: Optional[str] = None
    sources: List[Dict[str, str]] = []

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            flash("Please enter a question.", "warning")
            return render_template("job_match/match.html", result=None, sources=[])

        try:
            result, sources = smart_career_search(question)

            # Store latest result in session for PDF download
            session["job_match_last"] = {
                "question": question,
                "result": result or "",
                "sources": sources,
            }

            save_query(
                user_id=session["user_id"],
                query_type="smart_career_search",
                input_text=question,
                ai_response=result or "",
            )
        except Exception as exc:
            flash(f"Error: {exc}", "danger")

    return render_template("job_match/match.html", result=result, sources=sources)


@job_match_bp.route("/download-pdf")
@login_required
def download_pdf() -> Union[Response, tuple[str, int]]:
    """Export the latest Smart Career Search result as a styled PDF."""
    last: Optional[Dict[str, object]] = session.get("job_match_last")
    if not last or not last.get("result"):
        flash("No search result to export. Run a search first.", "warning")
        return redirect(url_for("job_match.match"))

    result_str: str = str(last["result"])
    question_str: str = str(last.get("question", ""))
    sources_list: List[Dict[str, str]] = last.get("sources", [])  # type: ignore[assignment]

    # Build HTML
    html_parts: List[str] = [f"<p><strong>Question:</strong> {question_str}</p><hr>"]
    html_parts.append(md.markdown(result_str, extensions=["tables", "fenced_code"]))

    if sources_list:
        html_parts.append("<h2>Web Sources</h2><ul>")
        for src in sources_list:
            title = src.get("title", "Link")
            url = src.get("url", "#")
            snippet = src.get("snippet", "")
            html_parts.append(f'<li><strong>{title}</strong><br><small>{snippet[:200]}</small><br>'
                              f'<a href="{url}">{url}</a></li>')
        html_parts.append("</ul>")

    try:
        pdf_bytes: bytes = generate_pdf(
            title="Smart Career Search — AI Report",
            html_content="\n".join(html_parts),
            user_name=session.get("username", "User"),
        )
        response: Response = make_response(pdf_bytes)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=Smart_Career_Search.pdf"
        return response
    except Exception as exc:
        flash(f"PDF generation failed: {exc}", "danger")
        return redirect(url_for("job_match.match"))
