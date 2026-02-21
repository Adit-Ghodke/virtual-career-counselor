"""
Adzuna Job Market API — provides **real** salary data, job counts, and live
listings to ground AI features in actual market evidence.

API docs: https://developer.adzuna.com/activedocs
Free tier: 250 requests / month (more than enough for a portfolio project).

Requires ADZUNA_APP_ID and ADZUNA_APP_KEY in environment variables.
Degrades gracefully when keys are absent — every helper returns a typed
fallback so callers never need to None-check.
"""
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger: logging.Logger = logging.getLogger(__name__)

_BASE: str = "https://api.adzuna.com/v1/api"
_COUNTRY: str = "us"  # default country; extend if needed


def _creds() -> Optional[Dict[str, str]]:
    """Return Adzuna credentials or None when unset."""
    app_id: str = os.environ.get("ADZUNA_APP_ID", "")
    app_key: str = os.environ.get("ADZUNA_APP_KEY", "")
    if not app_id or not app_key:
        return None
    return {"app_id": app_id, "app_key": app_key}


# ── Salary statistics ────────────────────────────────────────────────────────


def get_salary_stats(job_title: str) -> Dict[str, Any]:
    """Fetch real salary data for *job_title* from Adzuna.

    Tries the salary history endpoint first; if empty (common on trial plans),
    falls back to computing mean salary from live job search results.

    Returns dict with keys:
        found (bool), mean (float), median (float|None),
        currency (str), count (int), source (str).
    """
    fallback: Dict[str, Any] = {
        "found": False, "mean": 0.0, "median": None,
        "currency": "USD", "count": 0, "source": "N/A",
    }
    creds = _creds()
    if creds is None:
        return fallback

    # Strategy 1: Salary history endpoint (most accurate when available)
    try:
        url = f"{_BASE}/jobs/{_COUNTRY}/history"
        params: Dict[str, Any] = {**creds, "what": job_title, "months": 1}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data: Dict[str, Any] = resp.json()
        month_data: Dict[str, float] = data.get("month", {})
        if month_data:
            latest_key: str = sorted(month_data.keys())[-1]
            return {
                "found": True,
                "mean": round(month_data[latest_key], 2),
                "median": None,
                "currency": "USD",
                "count": 0,
                "source": "Adzuna Job Market API (salary history)",
            }
    except Exception as exc:
        logger.debug(f"Adzuna salary history failed for '{job_title}': {exc}")

    # Strategy 2: Compute mean from live job search results
    try:
        url2 = f"{_BASE}/jobs/{_COUNTRY}/search/1"
        params2: Dict[str, Any] = {
            **creds, "what": job_title, "results_per_page": 10,
            "sort_by": "relevance",
        }
        resp2 = requests.get(url2, params=params2, timeout=8)
        resp2.raise_for_status()
        results: List[Dict[str, Any]] = resp2.json().get("results", [])
        salaries: List[float] = []
        total_count: int = resp2.json().get("count", 0)
        for r in results:
            s_min = r.get("salary_min")
            s_max = r.get("salary_max")
            if s_min and s_max:
                salaries.append((s_min + s_max) / 2)
            elif s_min:
                salaries.append(s_min)
        if salaries:
            return {
                "found": True,
                "mean": round(sum(salaries) / len(salaries), 2),
                "median": round(sorted(salaries)[len(salaries) // 2], 2),
                "currency": "USD",
                "count": total_count,
                "source": f"Adzuna Job Market API ({len(salaries)} listings sampled, {total_count:,} total)",
            }
    except Exception as exc:
        logger.debug(f"Adzuna salary search fallback failed for '{job_title}': {exc}")

    return fallback


# ── Live job listings ────────────────────────────────────────────────────────


def search_jobs(
    query: str,
    *,
    location: str = "",
    max_results: int = 5,
    sort_by: str = "relevance",
    full_time: bool = False,
) -> Dict[str, Any]:
    """Search Adzuna for live job listings.

    Returns dict:
        found (bool), total (int), jobs (List[Dict]) each with
        title, company, location, salary_min, salary_max, url, description.
    """
    fallback: Dict[str, Any] = {"found": False, "total": 0, "jobs": []}
    creds = _creds()
    if creds is None:
        return fallback
    try:
        url = f"{_BASE}/jobs/{_COUNTRY}/search/1"
        params: Dict[str, Any] = {
            **creds,
            "what": query,
            "results_per_page": min(max_results, 20),
            "sort_by": sort_by,
            "content-type": "application/json",
        }
        if location:
            params["where"] = location
        if full_time:
            params["full_time"] = 1

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data: Dict[str, Any] = resp.json()
        results: List[Dict[str, Any]] = data.get("results", [])
        jobs: List[Dict[str, Any]] = []
        for r in results[:max_results]:
            jobs.append({
                "title": r.get("title", "N/A"),
                "company": r.get("company", {}).get("display_name", "N/A"),
                "location": r.get("location", {}).get("display_name", "N/A"),
                "salary_min": r.get("salary_min"),
                "salary_max": r.get("salary_max"),
                "url": r.get("redirect_url", ""),
                "description": (r.get("description", "")[:200] + "…")
                if len(r.get("description", "")) > 200
                else r.get("description", ""),
                "created": r.get("created", ""),
            })
        return {
            "found": bool(jobs),
            "total": data.get("count", 0),
            "jobs": jobs,
        }
    except Exception as exc:
        logger.debug(f"Adzuna job search failed for '{query}': {exc}")
        return fallback


# ── Top companies for a role ─────────────────────────────────────────────────


def get_top_companies(job_title: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch companies with the most openings for *job_title*.

    Returns list of {name, count}.
    """
    creds = _creds()
    if creds is None:
        return []
    try:
        url = f"{_BASE}/jobs/{_COUNTRY}/top_companies"
        params: Dict[str, Any] = {**creds, "what": job_title}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data: Dict[str, Any] = resp.json()
        leaderboard: List[Dict[str, Any]] = data.get("leaderboard", [])
        return [
            {"name": entry.get("canonical_name", "Unknown"), "count": entry.get("count", 0)}
            for entry in leaderboard[:limit]
        ]
    except Exception as exc:
        logger.debug(f"Adzuna top companies failed for '{job_title}': {exc}")
        return []


# ── Formatting helpers (for injecting into AI prompts) ───────────────────────


def format_salary_context(job_title: str) -> str:
    """Return a short text block with real salary data, or empty string."""
    stats = get_salary_stats(job_title)
    if not stats["found"]:
        return ""
    lines: List[str] = [
        f"[REAL SALARY DATA from {stats['source']}]",
        f"  Role queried  : {job_title}",
        f"  Mean salary   : ${stats['mean']:,.0f}/year ({stats['currency']})",
    ]
    if stats.get("median"):
        lines.append(f"  Median salary : ${stats['median']:,.0f}/year")
    if stats.get("count"):
        lines.append(f"  Total openings: {stats['count']:,}")
    return "\n".join(lines) + "\n"


def format_jobs_context(query: str, max_results: int = 5) -> str:
    """Return a text block with live job listings, or empty string."""
    data = search_jobs(query, max_results=max_results)
    if not data["found"]:
        return ""
    lines: List[str] = [f"[LIVE JOB LISTINGS — {data['total']:,} total openings found]"]
    for j in data["jobs"]:
        sal = ""
        if j.get("salary_min") and j.get("salary_max"):
            sal = f" | ${j['salary_min']:,.0f}–${j['salary_max']:,.0f}"
        elif j.get("salary_min"):
            sal = f" | From ${j['salary_min']:,.0f}"
        lines.append(f"  • {j['title']} @ {j['company']} ({j['location']}{sal})")
        if j.get("url"):
            lines.append(f"    Apply → {j['url']}")
    return "\n".join(lines) + "\n"


def format_companies_context(job_title: str) -> str:
    """Return a text block with top hiring companies, or empty string."""
    companies = get_top_companies(job_title)
    if not companies:
        return ""
    lines: List[str] = ["[TOP HIRING COMPANIES]"]
    for c in companies:
        lines.append(f"  • {c['name']} — {c['count']} openings")
    return "\n".join(lines) + "\n"
