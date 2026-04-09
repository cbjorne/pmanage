from datetime import datetime, date, timezone, timedelta
from pmanage.db import get_conn

def run(args):
    today = date.today().isoformat()
    start_date = args.start_date or today
    end_date = args.end_date or today

    try:
        start_time = datetime.strptime(args.start_time, "%H:%M").strftime("%H:%M")
        end_time = datetime.strptime(args.end_time, "%H:%M").strftime("%H:%M")
        started_at = datetime.fromisoformat(f"{start_date}T{start_time}")
        ended_at = datetime.fromisoformat(f"{end_date}T{end_time}")
    except ValueError:
        print("Invalid date/time format. Use date: 2024-01-01, time: 9:00")
        return

    if ended_at <= started_at:
        print("End time must be after start time.")
        return

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO entries (project, started_at, ended_at, note) VALUES (?, ?, ?, ?)",
            (args.project, started_at.isoformat(), ended_at.isoformat(), args.note)
        )
    print(f"Added entry for project '{args.project}' from {started_at} to {ended_at}.")