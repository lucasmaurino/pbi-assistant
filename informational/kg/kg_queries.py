import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "db.sqlite"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ----------------------------
# PBIs by Feature
# ----------------------------

def get_pbis_by_feature(feature_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.pbi_id,
            p.title,
            s.name AS state,
            pe.name AS assigned_to
        FROM pbis p
        JOIN features f ON p.feature_id = f.feature_id
        JOIN states s ON p.state_id = s.state_id
        JOIN people pe ON p.assigned_to = pe.person_id
        WHERE LOWER(f.name) LIKE LOWER(?)
    """

    cursor.execute(query, (f"%{feature_name}%",))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "pbi_id": r[0],
            "title": r[1],
            "state": r[2],
            "assigned_to": r[3]
        }
        for r in rows
    ]


# ----------------------------
# PBIs by Person
# ----------------------------

def get_pbis_by_person(person_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.pbi_id,
            p.title,
            s.name AS state,
            f.name AS feature
        FROM pbis p
        JOIN people pe ON p.assigned_to = pe.person_id
        JOIN states s ON p.state_id = s.state_id
        JOIN features f ON p.feature_id = f.feature_id
        WHERE LOWER(pe.name) LIKE LOWER(?)
    """

    cursor.execute(query, (f"%{person_name}%",))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "pbi_id": r[0],
            "title": r[1],
            "state": r[2],
            "feature": r[3]
        }
        for r in rows
    ]


# ----------------------------
# PBIs by State
# ----------------------------

def get_pbis_by_state(state_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.pbi_id,
            p.title,
            f.name AS feature,
            pe.name AS assigned_to
        FROM pbis p
        JOIN states s ON p.state_id = s.state_id
        JOIN features f ON p.feature_id = f.feature_id
        JOIN people pe ON p.assigned_to = pe.person_id
        WHERE LOWER(s.name) LIKE LOWER(?)
    """

    cursor.execute(query, (f"%{state_name}%",))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "pbi_id": r[0],
            "title": r[1],
            "feature": r[2],
            "assigned_to": r[3]
        }
        for r in rows
    ]


# ----------------------------
# Feature progress by State
# ----------------------------

def get_feature_progress(feature_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            s.name,
            COUNT(*)
        FROM pbis p
        JOIN features f ON p.feature_id = f.feature_id
        JOIN states s ON p.state_id = s.state_id
        WHERE LOWER(f.name) LIKE LOWER(?)
        GROUP BY s.name
    """

    cursor.execute(query, (f"%{feature_name}%",))
    rows = cursor.fetchall()
    conn.close()

    return {state: count for state, count in rows}


# ----------------------------
# Full PBI context
# ----------------------------

def get_pbi_details(pbi_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.pbi_id,
            p.title,
            f.name AS feature,
            pe.name AS assigned_to,
            s.name AS state
        FROM pbis p
        JOIN features f ON p.feature_id = f.feature_id
        JOIN people pe ON p.assigned_to = pe.person_id
        JOIN states s ON p.state_id = s.state_id
        WHERE LOWER(p.pbi_id) LIKE LOWER(?)
    """

    cursor.execute(query, (f"%{pbi_id}%",))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "pbi_id": row[0],
        "title": row[1],
        "feature": row[2],
        "assigned_to": row[3],
        "state": row[4]
    }
