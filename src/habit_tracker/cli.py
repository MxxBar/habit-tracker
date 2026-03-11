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
        cur = current_streak(name)
        lng = longest_streak(name)
        rate = completion_rate(name, 30)
        click.echo(f"\n  Stats for '{name}'")
        click.echo(f"  Current streak : {cur} day(s)")
        click.echo(f"  Longest streak : {lng} day(s)")
        click.echo(f"  30-day rate    : {rate:.0%}\n")
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