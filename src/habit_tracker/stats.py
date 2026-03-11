"""
habit_tracker/stats.py
Feature 3: Streak calculation and completion rate statistics.
speckit.implement: spec_03_streaks
"""

from datetime import date, timedelta
from pathlib import Path
from .logging import get_completions
from .db import get_connection, init_db
from .habits import get_habit


def get_freezes(habit_name: str, db_path: Path | None = None) -> set[date]:
    """Return all freeze dates for a habit."""
    init_db(db_path)
    habit = get_habit(habit_name, db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT date FROM freezes WHERE habit_id = ? ORDER BY date",
            (habit["id"],),
        ).fetchall()
        return {date.fromisoformat(r["date"]) for r in rows}
    finally:
        conn.close()


def current_streak(habit_name: str, db_path: Path | None = None) -> int:
    """Return the current streak, counting freeze days as completed."""
    completions = set(get_completions(habit_name, db_path))
    freezes = get_freezes(habit_name, db_path)
    covered = completions | freezes

    if not covered:
        return 0

    today = date.today()
    cursor = today if today in covered else today - timedelta(days=1)

    if cursor not in covered:
        return 0

    streak = 0
    while cursor in covered:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def longest_streak(habit_name: str, db_path: Path | None = None) -> int:
    """Return the longest streak, counting freeze days as completed."""
    completions = set(get_completions(habit_name, db_path))
    freezes = get_freezes(habit_name, db_path)
    covered = sorted(completions | freezes)

    if not covered:
        return 0

    best = 1
    current = 1
    for i in range(1, len(covered)):
        if (covered[i] - covered[i - 1]).days == 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def completion_rate(
    habit_name: str, days: int = 30, db_path: Path | None = None
) -> float:
    """Return completion rate (0.0-1.0) over the last N days."""
    completions = set(get_completions(habit_name, db_path))
    today = date.today()
    window = {today - timedelta(days=i) for i in range(days)}
    completed_in_window = len(window & completions)
    return completed_in_window / days