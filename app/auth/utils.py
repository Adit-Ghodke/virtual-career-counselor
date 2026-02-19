"""
Decorators for route protection.
"""
from typing import Any, Callable
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.wrappers import Response


def login_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Redirect to login if user is not authenticated."""
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Redirect non-admin users away from admin routes."""
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated
