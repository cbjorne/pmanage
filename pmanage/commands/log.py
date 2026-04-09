from datetime import datetime, timezone, timedelta
from pmanage.db import get_conn

def run(args):
    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()
    query = "SELECT id, project, started_at, ended_at, note FROM entries WHERE started_at >= ?"
    params = [since]
    
    if args.project:
        query += " AND project = ?"
        params.append(args.project)

    query += " ORDER BY started_at DESC"

    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    if not rows:
        print("No entries found")
        return

    total_minutes = 0
    print(f"{'ID':<20}{'Date':<20}{'Project':<20}{'Duration':<20}{'Note':<20}")
    print("-" * 100)
    for row in rows:
        started = datetime.fromisoformat(row["started_at"])
        if row["ended_at"]:
            ended = datetime.fromisoformat(row["ended_at"])
            minutes = int((ended - started).total_seconds() / 60)
            total_minutes += minutes
            duration = f"{minutes}m"
        else:
            duration = "running"

        date = started.strftime("%Y-%m-%d %H:%M")
        note = f"{row['note']}" if row["note"] else ""
        print(f"{row['id']:<20}{date:<20}{row['project']:<20}{duration:<20}{note:<20}")
    
    print(f"\nTotal: {total_minutes // 60}h {total_minutes % 60}m")