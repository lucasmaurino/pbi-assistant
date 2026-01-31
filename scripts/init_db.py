import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "informational" / "kg" / "db.sqlite"
SCHEMA_PATH = BASE_DIR / "informational" / "kg" / "schema.sql"

def init_db():
    if DB_PATH.exists():
        DB_PATH.unlink()  # delete existing DB for clean init

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cur.executescript(f.read())

    # Insert mock data
    cur.executemany(
        "INSERT INTO features VALUES (?, ?)",
        [
            ("F-001", "Payments Modernization"),
        ],
    )

    cur.executemany(
        "INSERT INTO people VALUES (?, ?)",
        [
            ("U-1", "Alice"),
            ("U-2", "Bob"),
        ],
    )

    cur.executemany(
        "INSERT INTO states VALUES (?, ?)",
        [
            ("S-1", "New"),
            ("S-2", "Active"),
            ("S-3", "Done"),
        ],
    )

    cur.executemany(
        "INSERT INTO pbis VALUES (?, ?, ?, ?, ?)",
        [
            ("PBI-101", "Migrate ETL to Databricks", "F-001", "U-1", "S-2"),
            ("PBI-102", "Refactor validation rules", "F-001", "U-2", "S-1"),
        ],
    )

    cur.execute(
        "INSERT INTO comments (pbi_id, comment, created_at) VALUES (?, ?, ?)",
        (
            "PBI-101",
            "Initial migration started",
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()

    print("SQLite DB initialized successfully at:", DB_PATH)

if __name__ == "__main__":
    init_db()
