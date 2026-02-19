"""
Interview Prep Simulator — company-specific AI interview practice.
"""
import json
from typing import Dict, List, Union
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.wrappers import Response

from app.auth.utils import login_required
from app.services.groq_service import interview_reply, get_interview_system_prompt
from app.services.dynamo_service import save_conversation, award_badge

interview_bp = Blueprint("interview", __name__, url_prefix="/interview", template_folder="../templates")

COMPANIES: List[str] = ["Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Infosys", "TCS", "Wipro", "Startup"]
ROLES: List[str] = ["Software Engineer", "Data Scientist", "Data Analyst", "Cloud Engineer", "Product Manager",
         "DevOps Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "ML Engineer"]


@interview_bp.route("/", methods=["GET"])
@login_required
def start() -> Union[str, Response]:
    return render_template("interview/prep.html", chat=None, setup=True,
                           companies=COMPANIES, roles=ROLES, question_num=0)


@interview_bp.route("/begin", methods=["POST"])
@login_required
def begin() -> Union[str, Response]:
    company: str = request.form.get("company", "").strip()
    role: str = request.form.get("role", "").strip()

    if not company or not role:
        flash("Please select a company and role.", "warning")
        return redirect(url_for("interview.start"))

    system_prompt: str = get_interview_system_prompt(company, role)
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"I'm ready for my {role} interview at {company}. Please start with your first question."},
    ]

    try:
        ai_response = interview_reply(messages)
        messages.append({"role": "assistant", "content": ai_response})
    except Exception as exc:
        flash(f"AI error: {exc}", "danger")
        return redirect(url_for("interview.start"))

    session["int_messages"] = json.dumps(messages)
    session["int_question"] = 1
    session["int_meta"] = json.dumps({"company": company, "role": role})

    chat_display = [m for m in messages if m["role"] != "system"]
    return render_template("interview/prep.html", conversation=chat_display,
                           companies=COMPANIES, roles=ROLES, question_num=1,
                           company=company, role=role, finished=False)


@interview_bp.route("/answer", methods=["POST"])
@login_required
def answer() -> Union[str, Response]:
    user_answer: str = request.form.get("user_reply", "").strip()
    if not user_answer:
        flash("Please type your answer.", "warning")
        return redirect(url_for("interview.start"))

    messages: List[Dict[str, str]] = json.loads(session.get("int_messages", "[]"))
    question_num: int = session.get("int_question", 1)
    meta: Dict[str, str] = json.loads(session.get("int_meta", "{}"))

    if not messages:
        flash("Session expired. Start a new interview.", "warning")
        return redirect(url_for("interview.start"))

    messages.append({"role": "user", "content": user_answer})

    if question_num >= 5:
        messages.append({
            "role": "user",
            "content": "(This is the final answer. Please provide the overall interview score, strengths, areas to improve, and hiring recommendation.)"
        })

    try:
        ai_response = interview_reply(messages)
        messages.append({"role": "assistant", "content": ai_response})
    except Exception as exc:
        flash(f"AI error: {exc}", "danger")
        return redirect(url_for("interview.start"))

    question_num += 1
    session["int_messages"] = json.dumps(messages)
    session["int_question"] = question_num

    finished: bool = question_num > 5
    if finished:
        save_conversation(session["user_id"], "interview", messages)
        award_badge(session["user_id"], "Interview Ready", "bi-person-badge", "Completed an AI mock interview")
        session.pop("int_messages", None)
        session.pop("int_question", None)

    chat_display: List[Dict[str, str]] = [m for m in messages if m["role"] != "system"]
    return render_template("interview/prep.html", conversation=chat_display,
                           companies=COMPANIES, roles=ROLES, question_num=question_num,
                           company=meta.get("company", ""), role=meta.get("role", ""),
                           finished=finished)
