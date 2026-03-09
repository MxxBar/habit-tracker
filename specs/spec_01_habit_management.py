# speckit.specify: Habit Management
#
# Feature: Add, remove, and list habits stored in a local SQLite database.
#
# Spec:
# - Habits have: id (auto), name (str), created_at (date), active (bool)
# - add_habit(name) -> creates and persists a new habit
# - remove_habit(name) -> marks habit as inactive (soft delete)
# - list_habits() -> returns all active habits
# - Habit names must be unique (case-insensitive)
# - Raise ValueError if adding duplicate or removing nonexistent habit
#
# speckit.implement: See src/habit_tracker/habits.py