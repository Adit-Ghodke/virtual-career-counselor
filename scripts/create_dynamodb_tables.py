"""
Script to create DynamoDB tables for Virtual Career Counselor.
Run this once before first use:  python scripts/create_dynamodb_tables.py
"""
import os
from typing import Any
import boto3  # type: ignore[import-untyped]
from dotenv import load_dotenv  # type: ignore[import-untyped]

load_dotenv()

REGION: str = os.environ.get("AWS_REGION", "ap-south-1") or "ap-south-1"
dynamodb: Any = boto3.resource("dynamodb", region_name=REGION)  # type: ignore[no-untyped-call]


def create_users_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_USERS_TABLE", "Users"),
        KeySchema=[
            {"AttributeName": "user_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-index",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


def create_queries_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_QUERIES_TABLE", "Queries"),
        KeySchema=[
            {"AttributeName": "query_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "query_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


def create_adminlogs_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_ADMINLOGS_TABLE", "AdminLogs"),
        KeySchema=[
            {"AttributeName": "log_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "log_id", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


def create_conversations_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_CONVERSATIONS_TABLE", "Conversations"),
        KeySchema=[
            {"AttributeName": "conversation_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "conversation_id", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


def create_user_progress_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_PROGRESS_TABLE", "UserProgress"),
        KeySchema=[
            {"AttributeName": "progress_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "progress_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "user-index",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


def create_user_badges_table() -> None:
    table: Any = dynamodb.create_table(
        TableName=os.environ.get("DYNAMODB_BADGES_TABLE", "UserBadges"),
        KeySchema=[
            {"AttributeName": "badge_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "badge_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "user-index",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✅ Created table: {table.table_name}")


if __name__ == "__main__":
    print("Creating DynamoDB tables...")
    try:
        create_users_table()
    except Exception as e:
        print(f"Users table: {e}")
    try:
        create_queries_table()
    except Exception as e:
        print(f"Queries table: {e}")
    try:
        create_adminlogs_table()
    except Exception as e:
        print(f"AdminLogs table: {e}")
    try:
        create_conversations_table()
    except Exception as e:
        print(f"Conversations table: {e}")
    try:
        create_user_progress_table()
    except Exception as e:
        print(f"UserProgress table: {e}")
    try:
        create_user_badges_table()
    except Exception as e:
        print(f"UserBadges table: {e}")
    print("Done!")
