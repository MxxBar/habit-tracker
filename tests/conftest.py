"""Shared pytest fixtures for habit-tracker tests."""

import pytest
from pathlib import Path
from habit_tracker.db import init_db


@pytest.fixture
def db_path(tmp_path):
    """Provide a fresh temporary SQLite DB for each test."""
    path = tmp_path / "test_habits.db"
    init_db(path)
    return path
