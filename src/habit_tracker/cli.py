"""
habit_tracker/cli.py
Click-based CLI entry point.
"""

from datetime import date
import click
from .habits import add_habit, remove_habit, list_habits
from .logging import log_completion, unlog_completion
from .stats import current_streak, longest_streak, completion_rate
from .chart import render_chart, render_all_summary


@click.group()
def cli():
    """Habit Tracker - build streaks, one day at a time."""
    pass


# Feature 1: Habit Management

@cli.command("add")
@click.argument("name")
def cmd_add(name):
    """Add a new habit."""
    try:
        add_habit(name)
        click.echo(f"Added habit: '{name}'")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("remove")
@click.argument("name")
def cmd_remove(name):
    """Remove a habit."""
    try:
        click.confirm(f"Are you sure you want to remove '{name}'?", abort=True)
        remove_habit(name)
        click.echo(f"Removed habit: '{name}'")
    except click.Abort:
        click.echo("Cancelled.")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("list")
def cmd_list():
    """List all active habits."""
    habits = list_habits()
    if not habits:
        click.echo("No habits yet. Add one with: habits add <name>")
        return
    for h in habits:
        click.echo(f"  - {h['name']}  (since {h['created_at']})")


# Feature 2: Logging

@cli.command("log")
@click.argument("name")
@click.option("--date", "log_date", default=None, help="Date YYYY-MM-DD (default: today)")
def cmd_log(name, log_date):
    """Mark a habit as completed."""
    try:
        d = date.fromisoformat(log_date) if log_date else None
        log_completion(name, d)
        label = log_date or "today"
        click.echo(f"Logged '{name}' for {label}")

        # Motivational message based on streak
        streak = current_streak(name)
        if streak == 1:
            click.echo(click.style("  Great start! Day 1 in the books.", fg="cyan"))
        elif streak == 3:
            click.echo(click.style("  3 days strong! You're building a habit.", fg="cyan"))
        elif streak == 7:
            click.echo(click.style("  One week streak! You're on fire!", fg="yellow", bold=True))
        elif streak == 14:
            click.echo(click.style("  Two weeks! This is becoming second nature.", fg="yellow", bold=True))
        elif streak == 30:
            click.echo(click.style("  30 DAYS! You're a habit machine!", fg="green", bold=True))
        elif streak > 30:
            click.echo(click.style(f"  {streak} days and counting. Unstoppable.", fg="green", bold=True))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("unlog")
@click.argument("name")
@click.option("--date", "log_date", default=None, help="Date YYYY-MM-DD (default: today)")
def cmd_unlog(name, log_date):
    """Remove a completion entry."""
    try:
        d = date.fromisoformat(log_date) if log_date else None
        unlog_completion(name, d)
        label = log_date or "today"
        click.echo(f"Unlogged '{name}' for {label}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


# Feature 3: Stats

@cli.command("stats")
@click.argument("name")
def cmd_stats(name):
    """Show streak and completion stats for a habit."""
    try:
        from .db import get_connection, init_db
        init_db()
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE AND active = 1", (name,)
        ).fetchone()
        conn.close()

        cur = current_streak(name)
        lng = longest_streak(name)
        rate = completion_rate(name, 30)

        # Weekly progress
        from .logging import get_completions
        from datetime import date, timedelta
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        completions_this_week = sum(
            1 for d in get_completions(name)
            if d >= start_of_week
        )
        weekly_goal = row["weekly_goal"] if row else 7
        goal_str = f"{completions_this_week}/{weekly_goal} days this week"
        goal_color = "green" if completions_this_week >= weekly_goal else "yellow"

        click.echo(f"\n  Stats for '{name}'")
        click.echo(f"  Current streak : {cur} day(s)")
        click.echo(f"  Longest streak : {lng} day(s)")
        click.echo(f"  30-day rate    : {rate:.0%}")
        click.echo(f"  Weekly goal    : {click.style(goal_str, fg=goal_color)}\n")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


# Feature 4: Chart & Summary

@cli.command("chart")
@click.argument("name")
def cmd_chart(name):
    """Show a 4-week ASCII heatmap for a habit."""
    try:
        click.echo()
        click.echo(render_chart(name))
        click.echo()
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("summary")
def cmd_summary():
    """Show a one-line summary for all habits."""
    click.echo()
    click.echo(render_all_summary())
    click.echo()

@cli.command("history")
@click.argument("name")
def cmd_history(name):
    """Show all logged completion dates for a habit."""
    try:
        from .logging import get_completions
        completions = get_completions(name)
        if not completions:
            click.echo(f"No completions logged for '{name}' yet.")
            return
        click.echo(f"\n  Completion history for '{name}':")
        for d in reversed(completions):
            click.echo(f"    {d.strftime('%Y-%m-%d  (%A)')}")
        click.echo(f"\n  Total: {len(completions)} day(s) logged\n")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        


@cli.command("goal")
@click.argument("name")
@click.argument("days", type=int)
def cmd_goal(name, days):
    """Set a weekly goal (1-7 days per week) for a habit."""
    if not 1 <= days <= 7:
        click.echo("Error: Goal must be between 1 and 7 days per week.", err=True)
        return
    try:
        from .db import get_connection, init_db
        init_db()
        conn = get_connection()
        habit = conn.execute(
            "SELECT * FROM habits WHERE name = ? COLLATE NOCASE AND active = 1", (name,)
        ).fetchone()
        if not habit:
            click.echo(f"Error: Habit '{name}' not found.", err=True)
            return
        with conn:
            conn.execute(
                "UPDATE habits SET weekly_goal = ? WHERE id = ?", (days, habit["id"])
            )
        conn.close()
        click.echo(f"Goal set: '{name}' → {days} day(s) per week")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)

@cli.command("freeze")
@click.argument("name")
@click.option("--date", "freeze_date", default=None, help="Date YYYY-MM-DD (default: today)")
def cmd_freeze(name, freeze_date):
    """Use a streak freeze to protect your streak for a missed day."""
    try:
        from .db import get_connection, init_db
        from .habits import get_habit
        import sqlite3
        init_db()
        habit = get_habit(name)
        d = date.fromisoformat(freeze_date) if freeze_date else date.today()
        conn = get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO freezes (habit_id, date) VALUES (?, ?)",
                    (habit["id"], d.isoformat()),
                )
            click.echo(f"❄️  Streak freeze applied for '{name}' on {d}")
            click.echo(click.style("  Your streak is protected!", fg="cyan"))
        except sqlite3.IntegrityError:
            click.echo(f"Already frozen for '{name}' on {d}.")
        finally:
            conn.close()
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command("freezes")
@click.argument("name")
def cmd_freezes(name):
    """Show all streak freezes used for a habit."""
    try:
        from .stats import get_freezes
        freezes = sorted(get_freezes(name))
        if not freezes:
            click.echo(f"No freezes used for '{name}'.")
            return
        click.echo(f"\n  Streak freezes for '{name}':")
        for d in reversed(freezes):
            click.echo(f"    ❄️  {d.strftime('%Y-%m-%d  (%A)')}")
        click.echo(f"\n  Total: {len(freezes)} freeze(s) used\n")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)