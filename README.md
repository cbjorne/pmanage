# pmanage

A simple CLI tool for tracking time spent on projects.


## Contributing
This is a small personal project that I use to help track time spent on different projects. Feel free to create issues, though I do not keep up to date on this repo.

If you wish to contribute additional features, refer to existing issues, ensure README.md and tests are updated. Thank you for the support.

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

### `start` - Start a timer

```bash
pmanage start <project> [--note, -n <text>]
```

Begins tracking time for **project**. Only one timer can run at a time - stop the current timer before starting a new one.

```bash
pmanage start myapp
pmanage start myapp --note "working on auth"
```

### `stop` - Stop the running timer

```bash
pmanage stop [--note, -n <text>]
```

Stops the active timer and prints the elapsed time. Optionally update or add a note.

```bash
pmanage stop
pmanage stop -n "finished auth module"
```

### `status` - Show the active timer

```bash
pmanage status
```

Displays the currently running project, elapsed time, and note (if any). Prints "No timer running." when idle.

### `log` - View time entries

```bash
pmanage log [--project, -p <name>]
```

Lists recent time entries with start time, project name, duration, and notes. Entries with a running timer show `running` instead of a duration. A total is printed at the bottom.

```bash
pmanage log
pmanage log -p myapp
```

### `projects` - List all projects

```bash
pmanage projects
```

Prints every project name that has at least one time entry.


### `add` - Add a time entry manually

```bash
pmanage add <project_name> <start_time> <end_time> [--start-date <start_date>] [--end-date <end_date>] [--note | -n 'optional note']
```

Manually add a time entry, optionally add start and end dates (format: 2024-01-01) and note.


### `delete` - Delete a time entry by id

```bash
pmanage delete <id>
```

Delete a time entry.


### `edit` - Edit a time entry

```bash
pmanage edit <id> [--project | -p <project_name>] [--start-time | -s <start_time>] [--end-time | -e <end_time>] [--start-date <start_date>] [--end-date <end_date>] [--note | -n 'optional note']
```

Edit a time entry by id. All parameters optional except id.


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

## License

This project is licensed under the [MIT License](LICENSE).
