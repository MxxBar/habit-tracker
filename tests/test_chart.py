"""Tests for Feature 4: ASCII Chart and Summary."""

import pytest
from datetime import date, timedelta
from habit_tracker.habits import add_habit
from habit_tracker.logging import log_completion
from habit_tracker.chart import render_chart, render_all_summary


@pytest.fixture
def habit(db_path):
    add_habit("Meditation", db_path)
    return "Meditation"


def test_render_chart_contains_habit_name(db_path, habit):
    output = render_chart(habit, db_path)
    assert "Meditation" in output


def test_render_chart_contains_day_headers(db_path, habit):
    output = render_chart(habit, db_path)
    assert "Mo" in output
    assert "Su" in output


def test_render_chart_shows_completed_day(db_path, habit):
    log_completion(habit, date.today(), db_path)
    output = render_chart(habit, db_path)
    assert "[X]" in output


def test_render_chart_shows_incomplete_day(db_path, habit):
    output = render_chart(habit, db_path)
    assert "[ ]" in output


def test_render_chart_shows_streak(db_path, habit):
    log_completion(habit, date.today(), db_path)
    output = render_chart(habit, db_path)
    assert "Streak" in output


def test_render_chart_shows_rate(db_path, habit):
    output = render_chart(habit, db_path)
    assert "%" in output


def test_render_all_summary_no_habits(db_path):
    output = render_all_summary(db_path)
    assert "No habits" in output


def test_render_all_summary_shows_habits(db_path):
    add_habit("Running", db_path)
    add_habit("Reading", db_path)
    output = render_all_summary(db_path)
    assert "Running" in output
    assert "Reading" in output


def test_render_all_summary_shows_rate_column(db_path):
    add_habit("Yoga", db_path)
    output = render_all_summary(db_path)
    assert "30d Rate" in output or "%" in output