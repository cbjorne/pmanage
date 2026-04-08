import argparse
from pmanage.commands import start, stop, log, status, projects

def build_parser():
    parser = argparse.ArgumentParser(
        prog="pmanage",
        description="A simple project time management tool."
    )
    subparsers = parser.add_subparsers()

    p_start = subparsers.add_parser("start", help="Start tracking time for a project.")
    p_start.add_argument("project", type=str)
    p_start.add_argument("--note", "-n", type=str, default="")
    p_start.set_defaults(func=start.run)

    p_stop = subparsers.add_parser("stop", help="Stop tracking time for the current project.")
    p_stop.add_argument("--note", "-n", type=str, default="")
    p_stop.set_defaults(func=stop.run)

    p_status = subparsers.add_parser("status", help="Show running timer")
    p_status.set_defaults(func=status.run)

    p_log = subparsers.add_parser("log", help="Show time log for a project.")
    p_log.add_argument("--project", "-p", type=str)
    p_log.add_argument("--days", "-d", type=int, default=7, help="Number of days to look back in the log")

    p_projects = subparsers.add_parser("projects", help="List all projects.")
    p_projects.set_defaults(func=projects.run)

    return parser