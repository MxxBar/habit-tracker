# speckit.specify: Streak Freeze
#
# Feature: Protect a streak on a day the habit was missed.
#
# Spec:
# - freezes table: id, habit_id (fk), date (unique per habit)
# - freeze(habit_name, date=today) -> inserts a freeze record
# - get_freezes(habit_name) -> returns set of freeze dates
# - current_streak and longest_streak count freeze days as completed
# - freezes command shows all freeze dates used for a habit
# - Freezing same habit twice on same date raises IntegrityError
#
# speckit.implement: See src/habit_tracker/stats.py, src/habit_tracker/cli.py