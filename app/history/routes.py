"""
Query History, Bookmarks & PDF Export routes.
"""
from typing import Any, Dict, List, Optional, Union
import markdown  # type: ignore[import-untyped]
from flask import Blueprint, request, render_template, session, flash, redirect, url_for, make_response
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.dynamo_service import (
    get_user_queries, get_query_by_id,
    save_bookmark, get_user_bookmarks, delete_bookmark,
)
from app.services.pdf_service import generate_pdf

history_bp = Blueprint("history", __name__, url_prefix="/history", template_folder="../templates")


@history_bp.route("/")
@login_required
def index() -> Union[str, Response]:
    """Show query history with search/filter."""
    query_type: str = request.args.get("type", "") or ""
    queries: List[Dict[str, Any]] = get_user_queries(session["user_id"], limit=100)

    if query_type:
        queries = [q for q in queries if q.get("query_type") == query_type]

    # Gather unique query types for filter
    all_queries: List[Dict[str, Any]] = get_user_queries(session["user_id"], limit=200)
    types: List[str] = sorted(set(q.get("query_type", "unknown") for q in all_queries))

    return render_template("history/index.html", queries=queries, types=types, selected_type=query_type)


@history_bp.route("/detail/<query_id>")
@login_required
def detail(query_id: str) -> Union[str, Response]:
    """View full details of a single query."""
    query: Optional[Dict[str, Any]] = get_query_by_id(query_id, session["user_id"])
    if not query or query.get("user_id") != session["user_id"]:
        flash("Query not found.", "warning")
        return redirect(url_for("history.index"))
    return render_template("history/detail.html", query=query)


@history_bp.route("/export/<query_id>")
@login_required
def export_pdf(query_id: str) -> Union[str, Response]:
    """Export a query result to PDF."""
    query: Optional[Dict[str, Any]] = get_query_by_id(query_id, session["user_id"])
    if not query or query.get("user_id") != session["user_id"]:
        flash("Query not found.", "warning")
        return redirect(url_for("history.index"))

    ai_response = query.get("ai_response", "No content")
    html_content = markdown.markdown(ai_response, extensions=["tables", "fenced_code"])
    title = f"{query.get('query_type', 'Report').replace('_', ' ').title()} Report"

    pdf_bytes = generate_pdf(title, html_content, session.get("user_name", "User"))
    if pdf_bytes:
        response = make_response(pdf_bytes)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f'attachment; filename="{title}.pdf"'
        return response
    else:
        flash("PDF generation failed.", "danger")
        return redirect(url_for("history.detail", query_id=query_id))


# ── Bookmarks ─────────────────────────────────────────────────────────────────

@history_bp.route("/bookmarks")
@login_required
def bookmarks() -> Union[str, Response]:
    """View all bookmarked queries."""
    try:
        items = get_user_bookmarks(session["user_id"])
    except Exception:
        items = []
    return render_template("history/bookmarks.html", bookmarks=items)


@history_bp.route("/bookmark/add", methods=["POST"])
@login_required
def add_bookmark() -> Response:
    """Bookmark a query."""
    query_id: str = request.form.get("query_id", "") or ""
    title: str = request.form.get("title", "Untitled") or "Untitled"
    query_type: str = request.form.get("query_type", "unknown") or "unknown"

    try:
        save_bookmark(session["user_id"], query_id, title, query_type)
        flash("Bookmarked!", "success")
    except Exception as exc:
        flash(f"Error: {exc}", "danger")

    return redirect(request.referrer or url_for("history.index"))


@history_bp.route("/bookmark/remove", methods=["POST"])
@login_required
def remove_bookmark() -> Response:
    """Remove a bookmark."""
    bookmark_id: str = request.form.get("bookmark_id", "") or ""
    try:
        delete_bookmark(bookmark_id)
        flash("Bookmark removed.", "info")
    except Exception as exc:
        flash(f"Error: {exc}", "danger")
    return redirect(url_for("history.bookmarks"))
