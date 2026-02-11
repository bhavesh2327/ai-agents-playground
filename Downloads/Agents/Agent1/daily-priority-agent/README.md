# Daily Task Prioritization Agent

A Python CLI application that reads tasks from a CSV file, computes priority scores based on urgency, importance, and effort, and generates a daily plan within your available time.

## Features

- **Smart Prioritization**: Combines urgency (deadline), importance (impact), and effort to rank tasks
- **Quick Win Bonus**: Prioritizes tasks that take ≤15 minutes for momentum
- **Blocked Task Detection**: Separates blocked tasks that need unblocking steps
- **Time Constraint**: Respects daily available time (default: 120 minutes)
- **Multiple Outputs**: Generates both JSON (for automation) and TXT (human-readable) plans

## Project Structure

```
daily-priority-agent/
├── tasks.csv          # Input: your tasks with metadata
├── agent.py           # The prioritization agent
├── plan.json          # Output: structured plan data
├── plan.txt           # Output: human-readable summary
└── README.md          # This file
```

## Installation

No external dependencies required! Uses only Python standard library.

**Requirements:**
- Python 3.7+

**Verify Python:**
```bash
python --version
```

## Usage

### 1. Add Your Tasks

Edit `tasks.csv` with your tasks:

```csv
title,description,deadline,effort,impact,blocked,tags
Send proposal to client,Finalize and email proposal,2025-12-22,25m,high,no,work
Pay electricity bill,Online payment,2025-12-22,10m,medium,no,personal
```

**Field Formats:**
- `deadline`: YYYY-MM-DD format or leave blank
- `effort`: Use `S` (15m), `M` (45m), `L` (90m), or specific minutes like `25m`
- `impact`: `low`, `medium`, or `high`
- `blocked`: `yes` or `no`
- `tags`: Comma-separated (e.g., `work,urgent`)

### 2. Run the Agent

```bash
python agent.py
```

### 3. Review Your Plan

The agent will:
- Print the plan to console
- Save `plan.json` (for automation/integration)
- Save `plan.txt` (human-readable summary)

**Output sections:**
- **TOP 3**: Do these first (fits within available time)
- **NEXT 5**: Next priority tasks
- **UNBLOCK**: Blocked tasks requiring action
- **DEFER**: Low urgency/impact tasks

## Customization

### Adjust Scoring Weights

Edit `WEIGHTS` in `agent.py`:

```python
WEIGHTS = {
    "urgency": 2.0,        # Increase for deadline-driven prioritization
    "importance": 3.0,     # Increase for impact-driven prioritization
    "quickwin_bonus": 1.0, # Bonus for quick tasks
    "blocked_penalty": 5.0,# Penalty for blocked tasks
}
```

### Change Available Time

Edit `AVAILABLE_MIN` in `agent.py`:

```python
AVAILABLE_MIN = 180  # 3 hours per day
```

### Modify Effort Defaults

Edit `EFFORT_DEFAULTS_MIN`:

```python
EFFORT_DEFAULTS_MIN = {"S": 20, "M": 60, "L": 120}
```

## How It Works

### Scoring Formula

```
Score = (Urgency × 2.0) + (Importance × 3.0) + Quick Win Bonus - Blocked Penalty
```

**Urgency Scale (0-5):**
- 5.0: Overdue or due today
- 4.0: Due tomorrow
- 3.0: Due within 3 days
- 2.0: Due within 7 days
- 1.0: Due later
- 0.5: No deadline

**Importance:**
- High = 3
- Medium = 2
- Low = 1

**Quick Win Bonus:**
- +1.0 if effort ≤ 15 minutes

**Blocked Penalty:**
- -5.0 if task is blocked

### Time Allocation

The agent respects your available time:
1. Sorts all tasks by priority score
2. Selects top tasks until time limit is reached
3. Remaining high-priority tasks go to "NEXT 5"
4. Low urgency/impact tasks go to "DEFER"

## Example Output

```
Daily Task Prioritization Plan (2026-02-11)
=============================================
Available Time: 120 min | Allocated: 60 min | Remaining: 60 min

TOP 3 (Do these first)
----------------------
1. Fix login bug  | deadline: 2025-12-24 | effort: 90m | score: 15.0
   Why: Due soon, High impact
   Total effort: 90 min

NEXT 5
------
1. Prepare meeting agenda  | deadline: 2025-12-23 | effort: 30m | score: 14.0
   Why: Due soon, High impact
   Total effort: 30 min
```

## Tips

1. **Daily Ritual**: Run the agent each morning to plan your day
2. **Update Regularly**: Mark completed tasks and add new ones to `tasks.csv`
3. **Tune Weights**: Adjust weights based on your work style
4. **Review Deferrals**: Periodically check deferred tasks
5. **Unblock Tasks**: Address blocked tasks to make them actionable

## Course Reference

Part of **100 AI Agents in 100 Days** by Vivian Aranha
- Day 1: Daily Task Prioritization Agent
- [Course Link](https://www.udemy.com/course/100-ai-agents-in-100-days/)

## License

Educational project - feel free to modify and extend!
