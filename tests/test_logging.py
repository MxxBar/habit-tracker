"""Tests for Feature 2: Daily Completion Logging."""

import pytest
from datetime import date, timedelta
from habit_tracker.habits import add_habit
from habit_tracker.logging import log_completion, unlog_completion, get_completions


@pytest.fixture
def habit(db_path):
    add_habit("Reading", db_path)
    return "Reading"


def test_log_completion_today(db_path, habit):
    log_completion(habit, db_path=db_path)
    completions = get_completions(habit, db_path)
    assert date.today() in completions


def test_log_completion_specific_date(db_path, habit):
    target = date(2025, 1, 15)
    log_completion(habit, target, db_path)
    assert target in get_completions(habit, db_path)


def test_log_duplicate_raises(db_path, habit):
    target = date(2025, 3, 1)
    log_completion(habit, target, db_path)
    with pytest.raises(ValueError, match="already logged"):
        log_completion(habit, target, db_path)


def test_unlog_completion(db_path, habit):
    target = date(2025, 6, 10)
    log_completion(habit, target, db_path)
    unlog_completion(habit, target, db_path)
    assert target not in get_completions(habit, db_path)


def test_unlog_nonexistent_raises(db_path, habit):
    with pytest.raises(ValueError, match="No completion found"):
        unlog_completion(habit, date(2020, 1, 1), db_path)


def test_get_completions_sorted(db_path, habit):
    dates = [date(2025, 1, d) for d in [5, 1, 3]]
    for d in dates:
        log_completion(habit, d, db_path)
    result = get_completions(habit, db_path)
    assert result == sorted(result)


def test_get_completions_empty(db_path, habit):
    assert get_completions(habit, db_path) == []