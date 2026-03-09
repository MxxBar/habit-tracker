"""
habit_tracker/logging.py
Feature 2: Log and unlog daily habit completions.
speckit.implement: spec_02_logging
"""

import sqlite3
from datetime import date
from pathlib import Path
from .db import get_connection, init_db
from .habits import get_habit


def log_completion(
    habit_name: str,
    log_date: date | None = None,
    db_path: Path | None = None,
) -> None:
    """Mark a habit as completed on a given date (default: today).
    Raises ValueError on duplicate or unknown habit.
    """
    init_db(db_path)
    habit = get_habit(habit_name, db_path)
    target = (log_date or date.today()).isoformat()
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute(
                "INSERT INTO completions (habit_id, date) VALUES (?, ?)",
                (habit["id"], target),
            )
    except sqlite3.IntegrityError:
        raise ValueError(f"'{habit_name}' already logged for {target}.")
    finally:
        conn.close()


def unlog_completion(
    habit_name: str,
    log_date: date | None = None,
    db_path: Path | None = None,
) -> None:
    """Remove a completion entry. Raises ValueError if not found."""
    init_db(db_path)
    habit = get_habit(habit_name, db_path)
    target = (log_date or date.today()).isoformat()
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(
            "DELETE FROM completions WHERE habit_id = ? AND date = ?",
            (habit["id"], target),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"No completion found for '{habit_name}' on {target}.")
    finally:
        conn.close()


def get_completions(
    habit_name: str, db_path: Path | None = None
) -> list[date]:
    """Return all completion dates for a habit, sorted ascending."""
    init_db(db_path)
    habit = get_habit(habit_name, db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT date FROM completions WHERE habit_id = ? ORDER BY date",
            (habit["id"],),
        ).fetchall()
        return [date.fromisoformat(r["date"]) for r in rows]
    finally:
        conn.close()