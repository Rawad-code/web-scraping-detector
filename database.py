import sqlite3
from datetime import datetime

DB_NAME = "traffic_logs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            path TEXT,
            method TEXT,
            score INTEGER,
            status TEXT,
            reason TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_log(ip, user_agent, path, method, score, status, reason):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (ip, user_agent, path, method, score, status, reason, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ip,
        user_agent,
        path,
        method,
        score,
        status,
        reason,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip, user_agent, path, method, score, status, reason, timestamp
        FROM logs
        ORDER BY id DESC
        LIMIT 100
    """)

    logs = cursor.fetchall()
    conn.close()
    return logs


def get_statistics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'Human'")
    humans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'Suspicious'")
    suspicious = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'Blocked'")
    blocked = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "humans": humans,
        "suspicious": suspicious,
        "blocked": blocked
    }
