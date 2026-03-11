"""
habit_tracker/chart.py
Feature 4: ASCII progress chart (28-day heatmap) and all-habits summary.
speckit.implement: spec_04_chart
"""

from datetime import date, timedelta
from pathlib import Path
import click
from .logging import get_completions
from .habits import list_habits
from .stats import current_streak, completion_rate


def render_chart(habit_name: str, db_path: Path | None = None) -> str:
    """Render a 4-week ASCII heatmap for a habit."""
    completions = set(get_completions(habit_name, db_path))
    today = date.today()

    days_since_monday = today.weekday()
    this_monday = today - timedelta(days=days_since_monday)
    start = this_monday - timedelta(weeks=3)

    header = "  Mo  Tu  We  Th  Fr  Sa  Su"
    lines = [click.style(f"  {habit_name}", bold=True), header]

    for week in range(4):
        cells = []
        for day_offset in range(7):
            d = start + timedelta(weeks=week, days=day_offset)
            if d > today:
                cells.append(click.style("[-]", fg="bright_black"))
            elif d in completions:
                cells.append(click.style("[X]", fg="green", bold=True))
            else:
                cells.append(click.style("[ ]", fg="red"))
        lines.append("  " + "  ".join(cells))

    streak = current_streak(habit_name, db_path)
    rate = completion_rate(habit_name, 30, db_path)
    lines.append("")
    lines.append(
        f"  {click.style('Streak:', bold=True)} {click.style(str(streak) + ' day(s)', fg='yellow')}   "
        f"{click.style('30-day rate:', bold=True)} {click.style(f'{rate:.0%}', fg='cyan')}"
    )
    return "\n".join(lines)


def render_all_summary(db_path: Path | None = None) -> str:
    """One-line summary per active habit: name, streak, 30-day rate."""
    habits = list_habits(db_path)
    if not habits:
        return "  No habits tracked yet. Add one with: habits add <name>"

    lines = [click.style("  {:<20} {:>10}  {:>10}".format("Habit", "Streak", "30d Rate"), bold=True)]
    lines.append("  " + "-" * 44)
    for h in habits:
        name = h["name"]
        streak = current_streak(name, db_path)
        rate = completion_rate(name, 30, db_path)
        streak_str = click.style(f"{streak}d", fg="yellow")
        rate_str = click.style(f"{rate:.0%}", fg="cyan")
        lines.append(
            "  {:<20} {:>9}  {:>9}".format(name, streak_str, rate_str)
        )
    return "\n".join(lines)