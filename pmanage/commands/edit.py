from pmanage.db import get_conn
from datetime import datetime

def run(args):
    with get_conn() as conn:
        cursor = conn.execute("SELECT * FROM entries WHERE id = ?", (args.id,))
        entry = cursor.fetchone()
        if not entry:
            print(f"No entry found with ID {args.id}")
            return
        
        project = args.project or entry["project"]
        note = args.note if args.note is not None else entry["note"]

        try:
            start_time_str = datetime.strptime(args.start_time, "%H:%M").strftime("%H:%M") if args.start_time else datetime.fromisoformat(entry["started_at"]).strftime("%H:%M")
            end_time_str = datetime.strptime(args.end_time, "%H:%M").strftime("%H:%M") if args.end_time else (datetime.fromisoformat(entry["ended_at"]).strftime("%H:%M") if entry["ended_at"] else None)
            start_date_str = args.start_date or datetime.fromisoformat(entry["started_at"]).date().isoformat()
            end_date_str = args.end_date or (datetime.fromisoformat(entry["ended_at"]).date().isoformat() if entry["ended_at"] else None)

            started_at = datetime.fromisoformat(f"{start_date_str}T{start_time_str}")
            ended_at = datetime.fromisoformat(f"{end_date_str}T{end_time_str}") if end_time_str and end_date_str else None
        except ValueError:
            print("Invalid date/time format. Use date: 2024-01-01, time: 9:00")
            return

        if ended_at and ended_at <= started_at:
            print("End time must be after start time.")
            return

        conn.execute(
            "UPDATE entries SET project = ?, started_at = ?, ended_at = ?, note = ? WHERE id = ?",
            (project, started_at.isoformat(), ended_at.isoformat() if ended_at else None, note, args.id)
        )
    print(f"Updated entry with ID {args.id}.")