"""
RAG-Powered Job Matching — uses ChromaDB knowledge base for grounded AI answers.
"""
from typing import Optional, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import rag_enhanced_query
from app.services.rag_service import get_rag_context, get_doc_count, seed_knowledge_base, list_documents, add_documents
from app.services.dynamo_service import save_query

job_match_bp = Blueprint("job_match", __name__, url_prefix="/job-match", template_folder="../templates")


@job_match_bp.route("/", methods=["GET", "POST"])
@login_required
def match() -> Union[str, Response]:
    """RAG-powered career query answering."""
    result: Optional[str] = None
    doc_count: int = 0

    try:
        doc_count = get_doc_count()
    except Exception:
        pass

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            flash("Please enter a question.", "warning")
            return render_template("job_match/match.html", result=None, doc_count=doc_count)

        try:
            rag_ctx = get_rag_context(question, n_results=5)
            result = rag_enhanced_query(question, rag_ctx)

            save_query(
                user_id=session["user_id"],
                query_type="rag_job_match",
                input_text=question,
                ai_response=result,
            )
        except Exception as exc:
            flash(f"Error: {exc}", "danger")

    return render_template("job_match/match.html", result=result, doc_count=doc_count)


@job_match_bp.route("/seed", methods=["POST"])
@login_required
def seed() -> Response:
    """Seed the RAG knowledge base with built-in career data."""
    try:
        count = seed_knowledge_base()
        flash(f"Knowledge base seeded with {count} documents!", "success")
    except Exception as exc:
        flash(f"Error seeding: {exc}", "danger")
    return redirect(url_for("job_match.match"))


@job_match_bp.route("/add-doc", methods=["POST"])
@login_required
def add_doc() -> Response:
    """Add a custom document to the knowledge base."""
    title: str = request.form.get("doc_title", "").strip()
    content: str = request.form.get("doc_content", "").strip()
    category: str = request.form.get("doc_category", "custom") or "custom"

    if not title or not content:
        flash("Title and content are required.", "warning")
        return redirect(url_for("job_match.match"))

    try:
        add_documents([{
            "id": title.lower().replace(" ", "_"),
            "content": content,
            "metadata": {"source": "user_upload", "category": category, "title": title},
        }])
        flash(f"Document '{title}' added to knowledge base!", "success")
    except Exception as exc:
        flash(f"Error: {exc}", "danger")

    return redirect(url_for("job_match.match"))
