# speckit.specify: ASCII Progress Chart
#
# Feature: Render a visual 4-week heatmap of completions and a summary table.
#
# Spec:
# - render_chart(habit_name) -> str: ASCII grid showing last 28 days
# - Each day shown as [X] if completed, [ ] if not, [-] if future
# - Header row shows day labels: Mo Tu We Th Fr Sa Su
# - Footer shows current streak and 30-day completion rate
# - render_all_summary() -> str: one-line summary per habit (name, streak, rate)
#
# speckit.implement: See src/habit_tracker/chart.py