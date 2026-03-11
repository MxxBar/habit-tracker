# speckit.specify: Weekly Goal Setting
#
# Feature: Set a target number of days per week for each habit.
#
# Spec:
# - habits table has a weekly_goal column (int, default 7)
# - set_goal(habit_name, days) -> updates weekly_goal for a habit
# - days must be between 1 and 7, raises ValueError otherwise
# - stats command shows weekly progress: completions_this_week / weekly_goal
# - progress shown in green if goal met, yellow if not
#
# speckit.implement: See src/habit_tracker/cli.py (cmd_goal, cmd_stats)