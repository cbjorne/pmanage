# pmanage

A simple CLI tool for tracking time spent on projects. No external dependencies — just Python 3.11+ and SQLite.

## Installation

```bash
# Clone the repo
git clone <repo-url>
cd pmanage

# Create a virtual environment and install
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

After installation the `pmanage` command is available in your shell.

## Usage

```
pmanage <command> [options]
```

### `start` — Start a timer

```bash
pmanage start <project> [--note, -n <text>]
```

Begins tracking time for **project**. Only one timer can run at a time — stop the current timer before starting a new one.

```bash
pmanage start myapp
pmanage start myapp --note "working on auth"
```

### `stop` — Stop the running timer

```bash
pmanage stop [--note, -n <text>]
```

Stops the active timer and prints the elapsed time. Optionally update or add a note.

```bash
pmanage stop
pmanage stop -n "finished auth module"
```

### `status` — Show the active timer

```bash
pmanage status
```

Displays the currently running project, elapsed time, and note (if any). Prints "No timer running." when idle.

### `log` — View time entries

```bash
pmanage log [--project, -p <name>]
```

Lists recent time entries with start time, project name, duration, and notes. Entries with a running timer show `running` instead of a duration. A total is printed at the bottom.

```bash
pmanage log
pmanage log -p myapp
```

### `projects` — List all projects

```bash
pmanage projects
```

Prints every project name that has at least one time entry.

## Data Storage

All data is stored in a local SQLite database at:

```
~/.local/share/pmanage/pmanage.db
```

The database is created automatically on first run. The schema consists of a single `entries` table:

| Column       | Type    | Description                              |
|--------------|---------|------------------------------------------|
| `id`         | INTEGER | Auto-incrementing primary key            |
| `project`    | TEXT    | Project name                             |
| `started_at` | TEXT    | Start time (UTC, ISO 8601)               |
| `ended_at`   | TEXT    | End time (UTC, ISO 8601) or NULL if running |
| `note`       | TEXT    | Optional note                            |

## Project Structure

```
pmanage/
├── pyproject.toml
├── README.md
├── tests/
└── pmanage/
    ├── __init__.py
    ├── main.py          # Entry point — init db, parse args, dispatch
    ├── cli.py           # Argument parser and subcommand registration
    ├── db.py            # Database connection and schema init
    └── commands/
        ├── __init__.py
        ├── start.py     # Start a timer
        ├── stop.py      # Stop the running timer
        ├── status.py    # Show active timer
        ├── log.py       # List time entries
        └── projects.py  # List all projects
```

## License

Not yet specified.
