"""Everything that talks SQL. No other file knows there is a database."""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "pulsetrack.db"    # next to this file


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row                 # rows behave like dictionaries
    conn.execute("PRAGMA foreign_keys = ON")      # SQLite checks foreign keys only on request
    return conn


# ---------- activities ----------

def list_activities(sport=None, limit=20, offset=0):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM activities
        WHERE (:sport IS NULL OR sport = :sport)
        ORDER BY started_at DESC
        LIMIT :limit OFFSET :offset
        """,
        {"sport": sport, "limit": limit, "offset": offset},
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_activity(activity_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM activities WHERE id = :id",
        {"id": activity_id},
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def create_activity(activity):
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO activities (user_id, sport, title, started_at, duration_s, distance_m)
        VALUES (:user_id, :sport, :title, :started_at, :duration_s, :distance_m)
        """,
        activity,
    )
    conn.commit()                      # without commit the INSERT is thrown away
    new_id = cursor.lastrowid          # the id the database chose
    conn.close()
    return get_activity(new_id)


def update_activity(activity_id, activity):
    conn = get_connection()
    conn.execute(
        """
        UPDATE activities
        SET sport = :sport, title = :title, started_at = :started_at,
            duration_s = :duration_s, distance_m = :distance_m
        WHERE id = :id
        """,
        {**activity, "id": activity_id},
    )
    conn.commit()
    conn.close()
    return get_activity(activity_id)


def delete_activity(activity_id):
    conn = get_connection()
    conn.execute("DELETE FROM activities WHERE id = :id", {"id": activity_id})
    conn.commit()
    conn.close()


# ---------- users ----------

def list_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def create_user(user):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO users (email, display_name) VALUES (:email, :display_name)",
        user,
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_user(new_id)


def delete_user(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = :id", {"id": user_id})
    conn.commit()
    conn.close()


def list_activities_of_user(user_id):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM activities
        WHERE user_id = :user_id
        ORDER BY started_at DESC
        """,
        {"user_id": user_id},
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
