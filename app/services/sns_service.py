"""
AWS SNS service — email notifications (welcome, report, admin alerts).
"""
from typing import Any, Dict, Optional

import boto3  # type: ignore[import-untyped]
from flask import current_app


def _get_sns_client() -> Any:
    """Return a boto3 SNS client."""
    region: str = str(current_app.config.get("AWS_REGION", "ap-south-1") or "ap-south-1")  # type: ignore[arg-type]
    return boto3.client("sns", region_name=region)  # type: ignore[no-any-return]


def publish_email(subject: str, message: str) -> Optional[Dict[str, Any]]:
    """Publish a message to the configured SNS topic. Returns SNS response."""
    topic_arn: Optional[str] = str(current_app.config.get("SNS_TOPIC_ARN", "") or "") or None  # type: ignore[arg-type]
    if not topic_arn:
        current_app.logger.warning("SNS_TOPIC_ARN not set — skipping notification.")
        return None
    try:
        client: Any = _get_sns_client()
        response: Dict[str, Any] = client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message,
        )
        return response
    except Exception as exc:
        current_app.logger.error(f"SNS publish failed: {exc}")
        return None


def send_welcome_email(user_name: str, user_email: str) -> Optional[Dict[str, Any]]:
    """Send a welcome message after registration."""
    subject: str = "Welcome to Virtual Career Counselor!"
    message: str = (
        f"Hi {user_name},\n\n"
        "Thank you for registering at Virtual Career Counselor.\n"
        "You can now explore AI-powered career advice, course recommendations, "
        "and job market insights.\n\n"
        "— The Virtual Career Counselor Team"
    )
    return publish_email(subject, message)


def send_report_email(user_name: str, report_type: str, report_body: str) -> Optional[Dict[str, Any]]:
    """Email a career / course / insights report to the SNS topic."""
    subject: str = f"Your {report_type.title()} Report — Virtual Career Counselor"
    message: str = (
        f"Hi {user_name},\n\n"
        f"Here is your requested {report_type} report:\n\n"
        f"{report_body}\n\n"
        "— The Virtual Career Counselor Team"
    )
    return publish_email(subject, message)


def send_admin_alert(error_message: str) -> Optional[Dict[str, Any]]:
    """Notify admin of a critical issue."""
    subject: str = "[ALERT] Virtual Career Counselor — Error Threshold Exceeded"
    return publish_email(subject, error_message)
