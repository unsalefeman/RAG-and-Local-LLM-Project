import sqlite3
import json


DB_PATH = "rag.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_document(content, embedding):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (content, json.dumps(embedding))
    )
    conn.commit()
    conn.close()


def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1], json.loads(row[2])) for row in rows]

def clear_documents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents")
    conn.commit()
    conn.close()
