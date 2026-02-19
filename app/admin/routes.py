"""
Admin Dashboard routes — user management, query logs, system health.
"""
from typing import Any, Dict, List, Union
from flask import Blueprint, render_template
from werkzeug.wrappers import Response

from app.auth.utils import admin_required
from app.services.dynamo_service import get_all_users, get_all_queries

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates")


@admin_bp.route("/")
@admin_required
def dashboard() -> Union[str, Response]:
    users: List[Dict[str, Any]] = get_all_users()
    queries: List[Dict[str, Any]] = get_all_queries()

    # ── Compute health metrics ─────────────────────────────────────────────────
    total_users: int = len(users)
    total_queries: int = len(queries)

    # Count queries per type
    career_count: int = sum(1 for q in queries if q.get("query_type") == "career")
    course_count: int = sum(1 for q in queries if q.get("query_type") == "course")
    insights_count: int = sum(1 for q in queries if q.get("query_type") == "insights")

    # Build per-user query count map
    user_query_counts: Dict[str, int] = {}
    for q in queries:
        uid: str = q.get("user_id", "unknown")
        user_query_counts[uid] = user_query_counts.get(uid, 0) + 1

    # Attach query count to each user
    for u in users:
        u["query_count"] = user_query_counts.get(u["user_id"], 0)

    # Sort users by registration date (newest first)
    users.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return render_template(
        "admin/dashboard.html",
        users=users,
        queries=queries[:50],  # last 50 queries
        total_users=total_users,
        total_queries=total_queries,
        career_count=career_count,
        course_count=course_count,
        insights_count=insights_count,
    )
