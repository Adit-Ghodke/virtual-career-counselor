"""
Auth routes — Register, Login, Logout.
Passwords hashed with bcrypt. Sessions managed via Flask-Session.
"""
from typing import Any, Dict, Optional, Union
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.wrappers import Response
import bcrypt

from app.services.dynamo_service import create_user, get_user_by_email
from app.services.sns_service import send_welcome_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    if request.method == "POST":
        name: str = request.form.get("name", "").strip()
        email: str = request.form.get("email", "").strip().lower()
        password: str = request.form.get("password", "") or ""

        # ── Validation ────────────────────────────────────────────
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("auth/register.html")

        # Check duplicate email
        existing: Optional[Dict[str, Any]] = get_user_by_email(email)
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("auth/register.html")

        # ── Create user ───────────────────────────────────────────
        hashed: str = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        _user: Dict[str, Any] = create_user(name=name, email=email, password_hash=hashed)

        # Send welcome email via SNS
        send_welcome_email(user_name=name, user_email=email)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    if request.method == "POST":
        email: str = request.form.get("email", "").strip().lower()
        password: str = request.form.get("password", "") or ""

        user: Optional[Dict[str, Any]] = get_user_by_email(email)
        if user is None:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        # Verify bcrypt hash
        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        # Set session
        session.clear()
        session["user_id"] = user["user_id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["role"] = user.get("role", "user")

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout() -> Response:
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
