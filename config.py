import os
from typing import Optional
from dotenv import load_dotenv  # type: ignore[import-untyped]

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-me") or "dev-secret-change-me"
    SESSION_TYPE: str = "filesystem"
    SESSION_PERMANENT: bool = False

    # Groq AI
    GROQ_API_KEY: Optional[str] = os.environ.get("GROQ_API_KEY")
    GROQ_MODEL: str = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile") or "llama-3.3-70b-versatile"

    # AWS
    AWS_REGION: str = os.environ.get("AWS_REGION", "ap-south-1") or "ap-south-1"
    SNS_TOPIC_ARN: Optional[str] = os.environ.get("SNS_TOPIC_ARN")

    # DynamoDB table names
    DYNAMODB_USERS_TABLE: str = os.environ.get("DYNAMODB_USERS_TABLE", "Users") or "Users"
    DYNAMODB_QUERIES_TABLE: str = os.environ.get("DYNAMODB_QUERIES_TABLE", "Queries") or "Queries"
    DYNAMODB_ADMINLOGS_TABLE: str = os.environ.get("DYNAMODB_ADMINLOGS_TABLE", "AdminLogs") or "AdminLogs"
    DYNAMODB_CONVERSATIONS_TABLE: str = os.environ.get("DYNAMODB_CONVERSATIONS_TABLE", "Conversations") or "Conversations"
    DYNAMODB_PROGRESS_TABLE: str = os.environ.get("DYNAMODB_PROGRESS_TABLE", "UserProgress") or "UserProgress"
    DYNAMODB_BADGES_TABLE: str = os.environ.get("DYNAMODB_BADGES_TABLE", "UserBadges") or "UserBadges"
    DYNAMODB_BOOKMARKS_TABLE: str = os.environ.get("DYNAMODB_BOOKMARKS_TABLE", "Bookmarks") or "Bookmarks"
    DYNAMODB_MENTOR_TABLE: str = os.environ.get("DYNAMODB_MENTOR_TABLE", "MentorChats") or "MentorChats"
    DYNAMODB_CLASSROOMS_TABLE: str = os.environ.get("DYNAMODB_CLASSROOMS_TABLE", "Classrooms") or "Classrooms"
    DYNAMODB_DIGEST_TABLE: str = os.environ.get("DYNAMODB_DIGEST_TABLE", "DigestPreferences") or "DigestPreferences"

    # GitHub API
    GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "") or ""

    # Tavily AI Web Search
    TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "") or ""

    # Admin
    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "admin@example.com") or "admin@example.com"


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False
