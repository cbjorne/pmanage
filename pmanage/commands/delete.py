from pmanage.db import get_conn

def run(args):
    with get_conn() as conn:
        cursor = conn.execute("SELECT id FROM entries WHERE id = ?", (args.id,))
        entry = cursor.fetchone()
        if not entry:
            print(f"No entry found with ID {args.id}")
            return
        
        conn.execute("DELETE FROM entries WHERE id = ?", (args.id,))
        print(f"Deleted entry with ID {args.id}")