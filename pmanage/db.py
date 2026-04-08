import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".local" / "share" / "pmanage" / "pmanage.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project     TEXT    NOT NULL,
                started_at  TEXT    NOT NULL,
                ended_at    TEXT,
                note        TEXT
            )
        """)