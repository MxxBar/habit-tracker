# 🌱 Habit Tracker

A command-line habit tracker built with Python and uv. Track daily habits, build streaks, and visualize your progress in the terminal.

## Setup
```bash
uv sync
```

## Usage

### Add & manage habits
```bash
uv run habits add "Meditate"
uv run habits add "Exercise"
uv run habits list
uv run habits remove "Exercise"
```

### Log completions
```bash
uv run habits log "Meditate"
uv run habits log "Meditate" --date 2026-03-08
uv run habits unlog "Meditate"
```

### View stats
```bash
uv run habits stats "Meditate"
```

### Visualize progress
```bash
uv run habits chart "Meditate"
uv run habits summary
```

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Habit Management | Add, remove, and list habits stored in SQLite |
| 2 | Daily Logging | Log or unlog completions for any date |
| 3 | Streaks & Stats | Current streak, longest streak, 30-day completion rate |
| 4 | ASCII Chart | 4-week heatmap and summary table for all habits |

## Running Tests
```bash
uv run pytest -v
```

## Project Structure
```
habit-tracker/
├── pyproject.toml
├── specs/                        # speckit.specify blocks
│   ├── spec_01_habit_management.py
│   ├── spec_02_logging.py
│   ├── spec_03_streaks.py
│   └── spec_04_chart.py
├── src/habit_tracker/
│   ├── db.py        # SQLite setup
│   ├── habits.py    # Feature 1
│   ├── logging.py   # Feature 2
│   ├── stats.py     # Feature 3
│   ├── chart.py     # Feature 4
│   └── cli.py       # CLI entry point
└── tests/
    ├── conftest.py
    ├── test_habits.py
    ├── test_logging.py
    ├── test_stats.py
    └── test_chart.py
```