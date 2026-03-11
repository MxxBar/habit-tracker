# speckit.specify: Motivational Messages
#
# Feature: Display motivational messages when logging a habit based on streak length.
#
# Spec:
# - After logging a habit, check the current streak
# - streak == 1  -> "Great start! Day 1 in the books."
# - streak == 3  -> "3 days strong! You're building a habit."
# - streak == 7  -> "One week streak! You're on fire!"
# - streak == 14 -> "Two weeks! This is becoming second nature."
# - streak == 30 -> "30 DAYS! You're a habit machine!"
# - streak > 30  -> "{streak} days and counting. Unstoppable."
# - Messages are color coded using click.style
#
# speckit.implement: See src/habit_tracker/cli.py (cmd_log)