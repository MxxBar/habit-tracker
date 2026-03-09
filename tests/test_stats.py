"""Tests for Feature 3: Streaks and Statistics."""

import pytest
from datetime import date, timedelta
from habit_tracker.habits import add_habit
from habit_tracker.logging import log_completion
from habit_tracker.stats import current_streak, longest_streak, completion_rate


@pytest.fixture
def habit(db_path):
    add_habit("Exercise", db_path)
    return "Exercise"


def test_current_streak_none(db_path, habit):
    assert current_streak(habit, db_path) == 0


def test_current_streak_today_only(db_path, habit):
    log_completion(habit, date.today(), db_path)
    assert current_streak(habit, db_path) == 1


def test_current_streak_consecutive(db_path, habit):
    today = date.today()
    for i in range(5):
        log_completion(habit, today - timedelta(days=i), db_path)
    assert current_streak(habit, db_path) == 5


def test_current_streak_broken(db_path, habit):
    today = date.today()
    log_completion(habit, today, db_path)
    log_completion(habit, today - timedelta(days=2), db_path)
    assert current_streak(habit, db_path) == 1


def test_current_streak_yesterday_counts(db_path, habit):
    yesterday = date.today() - timedelta(days=1)
    log_completion(habit, yesterday, db_path)
    assert current_streak(habit, db_path) == 1


def test_longest_streak_no_completions(db_path, habit):
    assert longest_streak(habit, db_path) == 0


def test_longest_streak_single(db_path, habit):
    log_completion(habit, date(2025, 1, 10), db_path)
    assert longest_streak(habit, db_path) == 1


def test_longest_streak_with_gap(db_path, habit):
    base = date(2025, 2, 1)
    for i in range(3):
        log_completion(habit, base + timedelta(days=i), db_path)
    base2 = date(2025, 2, 10)
    for i in range(5):
        log_completion(habit, base2 + timedelta(days=i), db_path)
    assert longest_streak(habit, db_path) == 5


def test_completion_rate_zero(db_path, habit):
    assert completion_rate(habit, 30, db_path) == 0.0


def test_completion_rate_full(db_path, habit):
    today = date.today()
    for i in range(30):
        log_completion(habit, today - timedelta(days=i), db_path)
    assert completion_rate(habit, 30, db_path) == 1.0


def test_completion_rate_half(db_path, habit):
    today = date.today()
    for i in range(0, 30, 2):
        log_completion(habit, today - timedelta(days=i), db_path)
    rate = completion_rate(habit, 30, db_path)
    assert 0.45 <= rate <= 0.55