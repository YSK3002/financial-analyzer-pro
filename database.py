import sqlite3

DATABASE_NAME = "analysis.db"

def init_db():
    """Initializes the database and creates the results table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            task_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(task_id: str, status: str, result: str = None):
    """Saves or updates the result of a task in the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_results (task_id, status, result)
        VALUES (?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
            status = excluded.status,
            result = excluded.result
    """, (task_id, status, result))
    conn.commit()
    conn.close()

def get_result(task_id: str):
    """Retrieves the result of a task from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT status, result FROM analysis_results WHERE task_id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"status": row[0], "result": row[1]}
    return None