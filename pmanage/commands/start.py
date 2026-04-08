from datetime import datetime, timezone
from pmanage.db import get_conn

def run(args):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, project, started_at FROM entries WHERE ended_at IS NULL"
        ).fetchone()
        if row:
            print(f"Timer already running for project '{row['project']}' since {row['started_at']}")
            print("Run `pmanage stop` first.")
            return

        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "INSERT INTO entries (project, started_at, note) VALUES (?, ?, ?)",
            (args.project, now, args.note)
        )
        print(f"Started tracking time for project '{args.project}' at {now}")