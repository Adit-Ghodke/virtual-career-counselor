"""
DynamoDB service — CRUD helpers for Users, Queries, and AdminLogs tables.
Uses boto3 resource API with latest patterns from Context7 docs.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3  # type: ignore[import-untyped]
from boto3.dynamodb.conditions import Key, Attr  # type: ignore[import-untyped]
from flask import current_app


def _get_table(table_name_key: str) -> Any:
    """Return a DynamoDB Table resource using the app config."""
    dynamodb: Any = boto3.resource("dynamodb", region_name=current_app.config["AWS_REGION"])  # type: ignore[no-untyped-call]
    return dynamodb.Table(current_app.config[table_name_key])


# ─── Users ────────────────────────────────────────────────────────────────────

def create_user(name: str, email: str, password_hash: str, role: str = "user") -> Dict[str, Any]:
    """Insert a new user into the Users table. Returns the item dict."""
    table: Any = _get_table("DYNAMODB_USERS_TABLE")
    user = {
        "user_id": str(uuid.uuid4()),
        "email": email,
        "name": name,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "role": role,
    }
    table.put_item(Item=user)
    return user


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Look up a user by email using the email-index GSI."""
    table: Any = _get_table("DYNAMODB_USERS_TABLE")
    resp = table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email),  # type: ignore[no-untyped-call]
    )
    items: List[Dict[str, Any]] = resp.get("Items", [])
    return items[0] if items else None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get a single user by partition key."""
    table: Any = _get_table("DYNAMODB_USERS_TABLE")
    resp = table.get_item(Key={"user_id": user_id})
    return resp.get("Item")


def get_all_users() -> List[Dict[str, Any]]:
    """Scan and return every user (admin use)."""
    table: Any = _get_table("DYNAMODB_USERS_TABLE")
    resp = table.scan()
    return resp.get("Items", [])


# ─── Queries ──────────────────────────────────────────────────────────────────

def save_query(user_id: str, query_type: str, input_text: str, ai_response: str) -> Dict[str, Any]:
    """Persist an AI query/response pair."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    item = {
        "query_id": str(uuid.uuid4()),
        "user_id": user_id,
        "query_type": query_type,
        "input_text": input_text,
        "ai_response": ai_response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_user_queries(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:  # type: ignore[no-redef]
    """Return last N queries for a user (sorted by timestamp desc)."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    resp: Dict[str, Any] = table.scan(
        FilterExpression=Attr("user_id").eq(user_id),  # type: ignore[no-untyped-call]
    )
    items: List[Dict[str, Any]] = resp.get("Items", [])
    items.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
    return items[:limit]


def get_all_queries() -> List[Dict[str, Any]]:
    """Scan all queries (admin use)."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    resp = table.scan()
    items: List[Dict[str, Any]] = resp.get("Items", [])
    items.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
    return items


# ─── Admin Logs ───────────────────────────────────────────────────────────────

def log_admin_event(level: str, message: str, source: str = "app") -> None:
    """Write an entry to the AdminLogs table."""
    table: Any = _get_table("DYNAMODB_ADMINLOGS_TABLE")
    table.put_item(Item={
        "log_id": str(uuid.uuid4()),
        "level": level,
        "message": message,
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


# ─── Conversations (multi-turn: negotiation, interview) ──────────────────────

def save_conversation(user_id: str, conv_type: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Save or update a conversation session."""
    import json
    table: Any = _get_table("DYNAMODB_CONVERSATIONS_TABLE")
    item: Dict[str, Any] = {
        "conversation_id": str(uuid.uuid4()),
        "user_id": user_id,
        "conv_type": conv_type,  # 'negotiation' or 'interview'
        "messages": json.dumps(messages),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_user_conversations(user_id: str, conv_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return conversations for a user, optionally filtered by type."""
    import json
    table: Any = _get_table("DYNAMODB_CONVERSATIONS_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    items: List[Dict[str, Any]] = resp.get("Items", [])
    if conv_type:
        items = [i for i in items if i.get("conv_type") == conv_type]
    for item in items:
        if isinstance(item.get("messages"), str):
            item["messages"] = json.loads(item["messages"])
    items.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
    return items


# ─── User Progress (learning paths) ──────────────────────────────────────────

def save_user_progress(user_id: str, roadmap_id: str, target_role: str,
                       total_weeks: int, completed_weeks: Optional[List[int]] = None) -> Dict[str, Any]:
    """Save or create a learning path progress entry."""
    table: Any = _get_table("DYNAMODB_PROGRESS_TABLE")
    import json
    item: Dict[str, Any] = {
        "progress_id": roadmap_id or str(uuid.uuid4()),
        "user_id": user_id,
        "target_role": target_role,
        "total_weeks": total_weeks,
        "completed_weeks": json.dumps(completed_weeks or []),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_user_progress(user_id: str) -> List[Dict[str, Any]]:
    """Return all learning path progress entries for a user."""
    import json
    table: Any = _get_table("DYNAMODB_PROGRESS_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    items: List[Dict[str, Any]] = resp.get("Items", [])
    for item in items:
        if isinstance(item.get("completed_weeks"), str):
            item["completed_weeks"] = json.loads(item["completed_weeks"])
    return items


def update_progress_weeks(progress_id: str, user_id: str, completed_weeks: List[int]) -> None:
    """Update the completed weeks for a learning path."""
    import json
    table: Any = _get_table("DYNAMODB_PROGRESS_TABLE")
    table.update_item(
        Key={"progress_id": progress_id, "user_id": user_id},
        UpdateExpression="SET completed_weeks = :w",
        ExpressionAttributeValues={":w": json.dumps(completed_weeks)},
    )


# ─── User Badges (gamification) ──────────────────────────────────────────────

def award_badge(user_id: str, badge_name: str, badge_icon: str, badge_desc: str) -> Dict[str, Any]:
    """Award a badge to a user (skip if already awarded)."""
    table: Any = _get_table("DYNAMODB_BADGES_TABLE")
    # Check if already awarded
    resp = table.scan(
        FilterExpression=Attr("user_id").eq(user_id) & Attr("badge_name").eq(badge_name)  # type: ignore[no-untyped-call]
    )
    if resp.get("Items"):
        return resp["Items"][0]
    item = {
        "badge_id": str(uuid.uuid4()),
        "user_id": user_id,
        "badge_name": badge_name,
        "badge_icon": badge_icon,
        "badge_desc": badge_desc,
        "awarded_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_user_badges(user_id: str) -> List[Dict[str, Any]]:
    """Return all badges for a user."""
    table: Any = _get_table("DYNAMODB_BADGES_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    return resp.get("Items", [])


def get_leaderboard(limit: int = 20) -> List[Dict[str, Any]]:
    """Build a leaderboard from query counts per user."""
    queries: List[Dict[str, Any]] = get_all_queries()
    user_counts: Dict[str, int] = {}
    for q in queries:
        uid = q.get("user_id", "unknown")
        user_counts[uid] = user_counts.get(uid, 0) + 1
    # Get user names
    users: List[Dict[str, Any]] = get_all_users()
    user_map: Dict[str, Dict[str, Any]] = {u["user_id"]: u for u in users}
    board: List[Dict[str, Any]] = []
    for uid, count in user_counts.items():
        u = user_map.get(uid, {})
        board.append({
            "user_id": uid,
            "name": u.get("name", "Unknown"),
            "query_count": count,
            "badges_count": len(get_user_badges(uid)),
        })
    board.sort(key=lambda x: int(x["query_count"]), reverse=True)
    return board[:limit]


# ─── Activity tracker for badge awarding ─────────────────────────────────────

def get_user_query_count(user_id: str) -> int:
    """Return total query count for a user."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    return len(resp.get("Items", []))


# ── Bookmarks ─────────────────────────────────────────────────────────────────

def save_bookmark(user_id: str, query_id: str, title: str, query_type: str) -> Dict[str, Any]:
    """Bookmark a query result."""
    table: Any = _get_table("DYNAMODB_BOOKMARKS_TABLE")
    item: Dict[str, Any] = {
        "bookmark_id": str(uuid.uuid4()),
        "user_id": user_id,
        "query_id": query_id,
        "title": title,
        "query_type": query_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_user_bookmarks(user_id: str) -> List[Dict[str, Any]]:
    """Get all bookmarks for a user."""
    table: Any = _get_table("DYNAMODB_BOOKMARKS_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    items: List[Dict[str, Any]] = resp.get("Items", [])
    items.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
    return items


def delete_bookmark(bookmark_id: str) -> None:
    """Delete a bookmark by ID."""
    table: Any = _get_table("DYNAMODB_BOOKMARKS_TABLE")
    table.delete_item(Key={"bookmark_id": bookmark_id})


# ── Mentor Chats ──────────────────────────────────────────────────────────────

def save_mentor_chat(user_id: str, messages: List[Dict[str, Any]], goals: str = "") -> Dict[str, Any]:
    """Save/update mentor chat session."""
    table: Any = _get_table("DYNAMODB_MENTOR_TABLE")
    item: Dict[str, Any] = {
        "user_id": user_id,
        "messages": messages,
        "goals": goals,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_mentor_chat(user_id: str) -> Optional[Dict[str, Any]]:
    """Get mentor chat for a user (single persistent session)."""
    table: Any = _get_table("DYNAMODB_MENTOR_TABLE")
    resp = table.get_item(Key={"user_id": user_id})
    return resp.get("Item")


# ── Classrooms ────────────────────────────────────────────────────────────────

def create_classroom(name: str, creator_id: str, creator_name: str) -> Dict[str, Any]:
    """Create a new classroom/team."""
    table: Any = _get_table("DYNAMODB_CLASSROOMS_TABLE")
    code: str = str(uuid.uuid4())[:8].upper()
    item: Dict[str, Any] = {
        "classroom_id": str(uuid.uuid4()),
        "name": name,
        "join_code": code,
        "creator_id": creator_id,
        "creator_name": creator_name,
        "members": [{"user_id": creator_id, "name": creator_name, "role": "admin"}],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_classroom_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Find a classroom by join code."""
    table: Any = _get_table("DYNAMODB_CLASSROOMS_TABLE")
    resp = table.scan(FilterExpression=Attr("join_code").eq(code.upper()))  # type: ignore[no-untyped-call]
    items: List[Dict[str, Any]] = resp.get("Items", [])
    return items[0] if items else None


def get_classroom(classroom_id: str) -> Optional[Dict[str, Any]]:
    """Get classroom by ID."""
    table: Any = _get_table("DYNAMODB_CLASSROOMS_TABLE")
    resp = table.get_item(Key={"classroom_id": classroom_id})
    return resp.get("Item")


def join_classroom(classroom_id: str, user_id: str, user_name: str) -> bool:
    """Add a member to a classroom."""
    classroom: Optional[Dict[str, Any]] = get_classroom(classroom_id)
    if not classroom:
        return False
    members: List[Dict[str, Any]] = classroom.get("members", [])
    if any(m["user_id"] == user_id for m in members):
        return True  # already a member
    members.append({"user_id": user_id, "name": user_name, "role": "member"})
    table: Any = _get_table("DYNAMODB_CLASSROOMS_TABLE")
    table.update_item(
        Key={"classroom_id": classroom_id},
        UpdateExpression="SET members = :m",
        ExpressionAttributeValues={":m": members},
    )
    return True


def get_user_classrooms(user_id: str) -> List[Dict[str, Any]]:
    """Get all classrooms a user belongs to."""
    table: Any = _get_table("DYNAMODB_CLASSROOMS_TABLE")
    resp = table.scan()
    items: List[Dict[str, Any]] = resp.get("Items", [])
    return [c for c in items if any(m["user_id"] == user_id for m in c.get("members", []))]


# ── Digest Preferences ───────────────────────────────────────────────────────

def save_digest_prefs(user_id: str, industries: List[str], enabled: bool = True) -> Dict[str, Any]:
    """Save weekly digest preferences."""
    table: Any = _get_table("DYNAMODB_DIGEST_TABLE")
    item: Dict[str, Any] = {
        "user_id": user_id,
        "industries": industries,
        "enabled": enabled,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


def get_digest_prefs(user_id: str) -> Optional[Dict[str, Any]]:
    """Get digest preferences for a user."""
    table: Any = _get_table("DYNAMODB_DIGEST_TABLE")
    resp = table.get_item(Key={"user_id": user_id})
    return resp.get("Item")


# ── Query History helpers ─────────────────────────────────────────────────────

def get_user_queries(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:  # type: ignore[no-redef]
    """Get recent queries for a user, sorted by newest first."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    resp = table.scan(FilterExpression=Attr("user_id").eq(user_id))  # type: ignore[no-untyped-call]
    items: List[Dict[str, Any]] = resp.get("Items", [])
    items.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
    return items[:limit]


def get_query_by_id(query_id: str) -> Optional[Dict[str, Any]]:
    """Get a single query by ID."""
    table: Any = _get_table("DYNAMODB_QUERIES_TABLE")
    resp = table.get_item(Key={"query_id": query_id})
    return resp.get("Item")
