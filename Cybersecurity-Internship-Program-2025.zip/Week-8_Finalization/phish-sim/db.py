import sqlite3
from datetime import datetime

DB_FILE = "events.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        msg_id TEXT,
        action TEXT,
        ts TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_event(user, msg_id, action):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO events (user, msg_id, action, ts) VALUES (?, ?, ?, ?)",
              (user, msg_id, action, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT action, COUNT(*) FROM events GROUP BY action")
    data = c.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data}

