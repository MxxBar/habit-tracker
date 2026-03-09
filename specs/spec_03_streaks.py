# speckit.specify: Streaks and Statistics
#
# Feature: Calculate current streak, longest streak, and completion rate.
#
# Spec:
# - current_streak(habit_name) -> int: consecutive days ending today or yesterday
# - longest_streak(habit_name) -> int: longest ever consecutive day run
# - completion_rate(habit_name, days=30) -> float: % of days completed in last N days
# - A streak breaks if any calendar day is missed
# - If completed yesterday but not today, streak is still alive
#
# speckit.implement: See src/habit_tracker/stats.py