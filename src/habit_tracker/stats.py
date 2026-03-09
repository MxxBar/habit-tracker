"""
habit_tracker/stats.py
Feature 3: Streak calculation and completion rate statistics.
speckit.implement: spec_03_streaks
"""

from datetime import date, timedelta
from pathlib import Path
from .logging import get_completions


def current_streak(habit_name: str, db_path: Path | None = None) -> int:
    """Return the current consecutive-day streak ending today or yesterday."""
    completions = set(get_completions(habit_name, db_path))
    if not completions:
        return 0

    today = date.today()
    cursor = today if today in completions else today - timedelta(days=1)

    if cursor not in completions:
        return 0

    streak = 0
    while cursor in completions:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def longest_streak(habit_name: str, db_path: Path | None = None) -> int:
    """Return the longest consecutive-day streak ever recorded."""
    completions = sorted(get_completions(habit_name, db_path))
    if not completions:
        return 0

    best = 1
    current = 1
    for i in range(1, len(completions)):
        if (completions[i] - completions[i - 1]).days == 1:
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
