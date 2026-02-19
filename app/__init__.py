import os
from typing import Any, Tuple, Union
from flask import Flask
from werkzeug.wrappers import Response
from flask_session import Session  # type: ignore[import-untyped]
from config import DevelopmentConfig, ProductionConfig


def create_app() -> Flask:
    """Application factory — creates and configures the Flask app."""
    app: Flask = Flask(__name__)

    # Load config based on FLASK_ENV
    env: str = os.environ.get("FLASK_ENV", "development") or "development"
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize server-side session
    Session(app)

    # ── Register Blueprints ──────────────────────────────────────
    from app.auth.routes import auth_bp
    from app.career.routes import career_bp
    from app.courses.routes import courses_bp
    from app.insights.routes import insights_bp
    from app.admin.routes import admin_bp
    from app.resume.routes import resume_bp
    from app.learning.routes import learning_bp
    from app.negotiation.routes import negotiation_bp
    from app.interview.routes import interview_bp
    from app.pivot.routes import pivot_bp
    from app.trends.routes import trends_bp
    from app.peers.routes import peers_bp
    from app.gamification.routes import gamification_bp
    # v3.0 blueprints
    from app.chatbot.routes import chatbot_bp
    from app.cover_letter.routes import cover_letter_bp
    from app.github_analyzer.routes import github_bp
    from app.skill_gap.routes import skill_gap_bp
    from app.history.routes import history_bp
    from app.mentor.routes import mentor_bp
    from app.group_discussion.routes import gd_bp
    from app.job_match.routes import job_match_bp
    from app.classroom.routes import classroom_bp
    from app.digest.routes import digest_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(negotiation_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(pivot_bp)
    app.register_blueprint(trends_bp)
    app.register_blueprint(peers_bp)
    app.register_blueprint(gamification_bp)
    # v3.0 blueprints
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(cover_letter_bp)
    app.register_blueprint(github_bp)
    app.register_blueprint(skill_gap_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(gd_bp)
    app.register_blueprint(job_match_bp)
    app.register_blueprint(classroom_bp)
    app.register_blueprint(digest_bp)

    # ── Dashboard route ──────────────────────────────────────────
    from flask import render_template, session, redirect, url_for

    @app.route("/")
    def index() -> Union[str, Response]:  # pyright: ignore[reportUnusedFunction]
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return render_template("dashboard.html")

    # ── Error handlers ───────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e: Any) -> Tuple[str, int]:  # pyright: ignore[reportUnusedFunction]
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e: Any) -> Tuple[str, int]:  # pyright: ignore[reportUnusedFunction]
        return render_template("errors/500.html"), 500

    return app
