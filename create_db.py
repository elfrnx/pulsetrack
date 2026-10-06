"""Builds pulsetrack.db from pulsetrack.sql. Run again any time for a fresh database."""

import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB_FILE = HERE / "pulsetrack.db"
SQL_FILE = HERE / "pulsetrack.sql"

conn = sqlite3.connect(DB_FILE)
conn.executescript(SQL_FILE.read_text(encoding="utf-8"))
conn.commit()
users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
activities = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
conn.close()

print(f"Database ready: {DB_FILE.name} with {users} users and {activities} activities")
