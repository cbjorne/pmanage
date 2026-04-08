from pmanage.db import get_conn

def run(args):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                project,
                COUNT(*) AS sessions,
                SUM(
                    CAST((julianday(ended_at) - julianday(started_at)) * 1440 AS INTEGER)
                    ) AS total_minutes
            FROM entries
            WHERE ended_at IS NOT NULL
            GROUP BY project
            ORDER BY total_minutes DESC
        """).fetchall()

    if not rows:
        print("No projects logged yet.")
        return
    
    print(f"{'Project':<25} {'Sessions':>8} {'Total':>8}")
    print("-" * 43)
    for row in rows:
        m = row["total_minutes"] or 0
        duration = f"{m // 60}h {m % 60}m"
        print(f"{row['project']:<25} {row['sessions']:>8} {duration:>8}")