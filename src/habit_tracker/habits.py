"""
habit_tracker/habits.py
Feature 1: Add, remove, and list habits.
speckit.implement: spec_01_habit_management
"""

import sqlite3
from pathlib import Path
from .db import get_connection, init_db


def add_habit(name: str, db_path: Path | None = None) -> dict:
    """Add a new habit. Raises ValueError if name already exists."""
    init_db(db_path)
    conn = get_connection(db_path)
    name = name.strip()
    if not name:
        raise ValueError("Habit name cannot be empty.")
    try:
        with conn:
            conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE", (name,)
        ).fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        existing = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE", (name,)
        ).fetchone()
        if existing and not existing["active"]:
            with conn:
                conn.execute(
                    "UPDATE habits SET active = 1 WHERE id = ?", (existing["id"],)
                )
            return dict(conn.execute(
                "SELECT * FROM habits WHERE id = ?", (existing["id"],)
            ).fetchone())
        raise ValueError(f"Habit '{name}' already exists.")
    finally:
        conn.close()


def remove_habit(name: str, db_path: Path | None = None) -> None:
    """Soft-delete a habit. Raises ValueError if not found."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE AND active = 1", (name,)
        ).fetchone()
        if not row:
            raise ValueError(f"Habit '{name}' not found.")
        with conn:
            conn.execute("UPDATE habits SET active = 0 WHERE id = ?", (row["id"],))
    finally:
        conn.close()


def list_habits(db_path: Path | None = None) -> list[dict]:
    """Return all active habits as a list of dicts."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM habits WHERE active = 1 ORDER BY name COLLATE NOCASE"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_habit(name: str, db_path: Path | None = None) -> dict:
    """Return a single active habit. Raises ValueError if not found."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE AND active = 1", (name,)
        ).fetchone()
        if not row:
            raise ValueError(f"Habit '{name}' not found.")
        return dict(row)
    finally:
        conn.close()