from datetime import datetime, timezone
from pmanage.db import get_conn

def run(args):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, project, started_at FROM entries WHERE ended_at IS NULL"
        ).fetchone()
        if not row:
            print("No timer running.")
            return

        now = datetime.now(timezone.utc).isoformat()
        note_update = args.note if hasattr(args, "note") and args.note else None

        if note_update:
            conn.execute(
                "UPDATE entries SET ended_at = ?, note = ? WHERE id = ?",
                (now, note_update, row["id"])
            )
        else:
            conn.execute(
                "UPDATE entries SET ended_at = ? WHERE id = ?",
                (now, row["id"])
            )

        started = datetime.fromisoformat(row["started_at"])
        ended = datetime.fromisoformat(now)
        duration = ended - started
        minutes = int(duration.total_seconds() / 60)
        print(f"Stopped '{row['project']}' — {minutes}m logged")