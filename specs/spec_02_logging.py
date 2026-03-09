# speckit.specify: Daily Completion Logging
#
# Feature: Log a habit as completed for a given date.
#
# Spec:
# - Completions have: id (auto), habit_id (fk), date (YYYY-MM-DD)
# - log_completion(habit_name, date=today) -> records a completion
# - unlog_completion(habit_name, date=today) -> removes a completion
# - get_completions(habit_name) -> list of all completion dates
# - Logging same habit twice on same date raises ValueError
# - Unlogging a non-existent completion raises ValueError
#
# speckit.implement: See src/habit_tracker/logging.py