import argparse
from pmanage.commands import start, stop, log, status, projects, add, delete, edit

def build_parser():
    parser = argparse.ArgumentParser(
        prog="pmanage",
        description="A simple project time management tool."
    )
    subparsers = parser.add_subparsers()

    p_start = subparsers.add_parser("start", help="Start tracking time for a project. Usage: pmanage start <project_name> [--note 'optional note']")
    p_start.add_argument("project", type=str)
    p_start.add_argument("--note", "-n", type=str, default="")
    p_start.set_defaults(func=start.run)

    p_stop = subparsers.add_parser("stop", help="Stop tracking time for the current project. Usage: pmanage stop [--note 'optional note']")
    p_stop.add_argument("--note", "-n", type=str, default="")
    p_stop.set_defaults(func=stop.run)

    p_status = subparsers.add_parser("status", help="Show running timer. Usage: pmanage status")
    p_status.set_defaults(func=status.run)

    p_log = subparsers.add_parser("log", help="Show time log for a project. Usage: pmanage log [--project | -p <project_name>] [--days | -d <number_of_days> default: 7]")
    p_log.add_argument("--project", "-p", type=str)
    p_log.add_argument("--days", "-d", type=int, default=7)
    p_log.set_defaults(func=log.run)

    p_projects = subparsers.add_parser("projects", help="List all projects. Usage: pmanage projects")
    p_projects.set_defaults(func=projects.run)

    p_add = subparsers.add_parser("add", help="Add a time entry manually. Usage: pmanage add <project_name> <start_time> <end_time> [--start-date <start_date>] [--end-date <end_date>] [--note 'optional note']")
    p_add.add_argument("project", type=str)
    p_add.add_argument("start_time", type=str, help="Start time (e.g. 09:00)")
    p_add.add_argument("end_time", type=str, help="End time (e.g. 17:00)")
    p_add.add_argument("--start-date", type=str, default=None, help="Start date (e.g. 2024-01-01), defaults to today")
    p_add.add_argument("--end-date", type=str, default=None, help="End date (e.g. 2024-01-01), defaults to today")
    p_add.add_argument("--note", "-n", type=str, default="")
    p_add.set_defaults(func=add.run)

    p_delete = subparsers.add_parser("delete", help="Delete a time entry by ID. Usage: pmanage delete <id>")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=delete.run)

    p_edit = subparsers.add_parser("edit", help="Edit a time entry by ID. Usage: pmanage edit <id> [--project | -p <project_name>] [--start-time | -s <start_time>] [--end-time | -e <end_time>] [--start-date <start_date>] [--end-date <end_date>] [--note | -n 'optional note']")
    p_edit.add_argument("id", type=int)
    p_edit.add_argument("--project", "-p", type=str)
    p_edit.add_argument("--start-time", "-s", type=str)
    p_edit.add_argument("--end-time", "-e", type=str)
    p_edit.add_argument("--start-date", type=str)
    p_edit.add_argument("--end-date", type=str)
    p_edit.add_argument("--note", "-n", type=str)
    p_edit.set_defaults(func=edit.run)

    return parser