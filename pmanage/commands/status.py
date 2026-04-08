from datetime import datetime, timezone
from pmanage.db import get_conn

def run(args):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT project, started_at, note FROM entries WHERE ended_at IS NULL"
        ).fetchone()
        if not row:
            print("No timer running.")
            return
        
        started = datetime.fromisoformat(row["started_at"])
        now = datetime.now(timezone.utc)
        elapsed = now - started
        minutes = int(elapsed.total_seconds() / 60)
        print(f"Running: '{row['project']}' for {minutes}m")
        if row["note"]:
            print(f"  Note: {row['note']}")