"""
habit_tracker/db.py
Database initialization and connection management using SQLite.
"""

import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    """Return path to the SQLite database file."""
    data_dir = Path.home() / ".habit_tracker"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "habits.db"


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open and return a SQLite connection with row factory set."""
    path = db_path or get_db_path()
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path | None = None) -> None:
    """Create tables if they don't exist."""
    conn = get_connection(db_path)
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS habits (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                created_at  TEXT    NOT NULL DEFAULT (date('now')),
                active      INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS completions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id    INTEGER NOT NULL REFERENCES habits(id),
                date        TEXT    NOT NULL,
                UNIQUE(habit_id, date)
            );
        """)
    conn.close()