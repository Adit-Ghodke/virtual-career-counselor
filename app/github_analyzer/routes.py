"""
GitHub Profile Analyzer — fetch repos + AI analysis.
"""
from typing import Any, Dict, List, Optional, Union
import requests
from flask import Blueprint, request, render_template, session, flash, current_app
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import analyze_github_profile
from app.services.dynamo_service import save_query

github_bp = Blueprint("github_analyzer", __name__, url_prefix="/github", template_folder="../templates")


def _fetch_github_repos(username: str) -> Optional[str]:
    """Fetch public repos from GitHub API and format for AI analysis."""
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
    token: str = str(current_app.config.get("GITHUB_TOKEN", "") or "")  # type: ignore[arg-type]
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers=headers,
        params={"sort": "updated", "per_page": 30},
        timeout=10,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    repos: List[Dict[str, Any]] = resp.json()

    # Also fetch user profile
    user_resp: requests.Response = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers,
        timeout=10,
    )
    user_data: Dict[str, Any] = user_resp.json() if user_resp.ok else {}

    lines: List[str] = [
        f"**GitHub User:** {username}",
        f"**Name:** {user_data.get('name', 'N/A')}",
        f"**Bio:** {user_data.get('bio', 'N/A')}",
        f"**Public Repos:** {user_data.get('public_repos', len(repos))}",
        f"**Followers:** {user_data.get('followers', 0)}",
        f"**Following:** {user_data.get('following', 0)}",
        f"**Account Created:** {str(user_data.get('created_at', 'N/A'))[:10]}",
        "",
        "**Repositories:**",
    ]

    for repo in repos[:20]:
        lang: Any = repo.get("language", "Unknown")
        stars: Any = repo.get("stargazers_count", 0)
        forks: Any = repo.get("forks_count", 0)
        desc: Any = repo.get("description", "No description") or "No description"
        updated: str = str(repo.get("updated_at", "N/A"))[:10]
        lines.append(
            f"- **{repo['name']}** [{lang}] ⭐{stars} 🍴{forks} — {desc} (updated: {updated})"
        )

    # Aggregate language stats
    lang_counts: Dict[str, int] = {}
    for repo in repos:
        lang_val: Optional[str] = repo.get("language")
        if lang_val:
            lang_counts[lang_val] = lang_counts.get(lang_val, 0) + 1
    lines.append("")
    lines.append("**Language Distribution:**")
    for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {lang}: {count} repos")

    return "\n".join(lines)


@github_bp.route("/", methods=["GET", "POST"])
@login_required
def analyze() -> Union[str, Response]:
    result: Optional[str] = None
    username: str = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip().lstrip("@")

        if not username:
            flash("Please enter a GitHub username.", "warning")
            return render_template("github_analyzer/analyze.html", result=None, username="")

        try:
            repos_info: Optional[str] = _fetch_github_repos(username)
            if repos_info is None:
                flash(f"GitHub user '{username}' not found.", "danger")
                return render_template("github_analyzer/analyze.html", result=None, username=username)

            result = analyze_github_profile(repos_info)
            save_query(
                user_id=session["user_id"],
                query_type="github_analysis",
                input_text=f"GitHub: {username}",
                ai_response=result,
            )
        except requests.RequestException as exc:
            flash(f"GitHub API error: {exc}", "danger")
        except Exception as exc:
            flash(f"AI error: {exc}", "danger")

    return render_template("github_analyzer/analyze.html", result=result, username=username)
