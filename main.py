"""
main.py
Entry point for the Habit Tracker app.
Run directly with: uv run python main.py
"""

import click
from src.habit_tracker.habits import list_habits
from src.habit_tracker.stats import current_streak, completion_rate
from src.habit_tracker.db import init_db


def main():
    init_db()
    habits = list_habits()

    click.echo(click.style("\n  🌱 Habit Tracker", bold=True, fg="green"))
    click.echo("  " + "─" * 40)

    if not habits:
        click.echo("  No habits yet. Get started:")
        click.echo(click.style("  uv run habits add \"Your Habit\"", fg="cyan"))
    else:
        click.echo(click.style("  Today's Dashboard\n", bold=True))
        for h in habits:
            name = h["name"]
            streak = current_streak(name)
            rate = completion_rate(name, 30)

            if streak > 0:
                status = click.style(f"🔥 {streak}d streak", fg="yellow")
            else:
                status = click.style("○ No streak", fg="red")

            click.echo(f"  {name:<20} {status:<25} {rate:.0%} this month")

    click.echo("\n  Commands:")
    click.echo(click.style("  uv run habits log <name>", fg="cyan") + "      — log today")
    click.echo(click.style("  uv run habits chart <name>", fg="cyan") + "    — view chart")
    click.echo(click.style("  uv run habits summary", fg="cyan") + "         — all habits")
    click.echo(click.style("  uv run habits --help", fg="cyan") + "          — all commands")
    click.echo()


if __name__ == "__main__":
    main()