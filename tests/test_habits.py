"""Tests for Feature 1: Habit Management (add, remove, list)."""

import pytest
from habit_tracker.habits import add_habit, remove_habit, list_habits, get_habit


def test_add_habit(db_path):
    habit = add_habit("Meditate", db_path)
    assert habit["name"] == "Meditate"
    assert habit["active"] == 1


def test_add_habit_duplicate_raises(db_path):
    add_habit("Exercise", db_path)
    with pytest.raises(ValueError, match="already exists"):
        add_habit("Exercise", db_path)


def test_add_habit_case_insensitive_duplicate(db_path):
    add_habit("Read", db_path)
    with pytest.raises(ValueError):
        add_habit("read", db_path)


def test_add_habit_empty_name_raises(db_path):
    with pytest.raises(ValueError):
        add_habit("   ", db_path)


def test_remove_habit(db_path):
    add_habit("Yoga", db_path)
    remove_habit("Yoga", db_path)
    habits = list_habits(db_path)
    assert all(h["name"] != "Yoga" for h in habits)


def test_remove_nonexistent_raises(db_path):
    with pytest.raises(ValueError, match="not found"):
        remove_habit("Ghost", db_path)


def test_list_habits_empty(db_path):
    assert list_habits(db_path) == []


def test_list_habits_returns_active_only(db_path):
    add_habit("Running", db_path)
    add_habit("Journaling", db_path)
    remove_habit("Running", db_path)
    names = [h["name"] for h in list_habits(db_path)]
    assert "Journaling" in names
    assert "Running" not in names


def test_readd_removed_habit(db_path):
    add_habit("Stretching", db_path)
    remove_habit("Stretching", db_path)
    habit = add_habit("Stretching", db_path)
    assert habit["active"] == 1
    assert len(list_habits(db_path)) == 1


def test_get_habit_not_found_raises(db_path):
    with pytest.raises(ValueError):
        get_habit("Nonexistent", db_path)