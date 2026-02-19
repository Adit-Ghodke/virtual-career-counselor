"""
Gamification — Badges & Leaderboard routes.
"""
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, render_template, session
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.dynamo_service import get_user_badges, get_leaderboard, get_user_query_count, award_badge

gamification_bp = Blueprint("gamification", __name__, url_prefix="/gamification", template_folder="../templates")

# Badge definitions — auto-award based on activity
BADGE_RULES: List[Dict[str, Any]] = [
    {"threshold": 1,  "name": "First Query",      "icon": "bi-lightning",       "desc": "Made your first AI query"},
    {"threshold": 5,  "name": "Explorer",          "icon": "bi-binoculars",      "desc": "Completed 5 AI queries"},
    {"threshold": 10, "name": "Power User",        "icon": "bi-rocket-takeoff",  "desc": "Completed 10 AI queries"},
    {"threshold": 25, "name": "Career Master",     "icon": "bi-trophy",          "desc": "Completed 25 AI queries"},
    {"threshold": 50, "name": "Legend",             "icon": "bi-star-fill",       "desc": "Completed 50 AI queries"},
]


@gamification_bp.route("/")
@login_required
def badges() -> Union[str, Response]:
    user_id: str = session["user_id"]

    # Auto-check and award query-based badges
    query_count: int = get_user_query_count(user_id)
    for rule in BADGE_RULES:
        if query_count >= rule["threshold"]:
            award_badge(user_id, rule["name"], rule["icon"], rule["desc"])

    user_badges: List[Dict[str, Any]] = get_user_badges(user_id)
    leaderboard: List[Dict[str, Any]] = get_leaderboard(limit=20)

    # Find user's rank
    user_rank: Optional[int] = None
    for i, entry in enumerate(leaderboard):
        if entry["user_id"] == user_id:
            user_rank = i + 1
            break

    return render_template("gamification/badges.html",
                           badges=user_badges,
                           leaderboard=leaderboard,
                           query_count=query_count,
                           user_rank=user_rank,
                           total_possible=len(BADGE_RULES) + 4)  # + 4 for feature-specific badges
