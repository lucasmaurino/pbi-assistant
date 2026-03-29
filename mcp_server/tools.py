import sqlite3
from pathlib import Path
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP


DB_PATH = Path(__file__).parents[1] / "informational" / "kg" / "db.sqlite"

mcp = FastMCP("pbi-action-server")


# =========================
# INPUT SCHEMAS
# =========================

class UpdatePBIStateInput(BaseModel):
    pbi_id: str
    new_state: str


class AssignPBIInput(BaseModel):
    pbi_id: str
    person_name: str


class AddCommentInput(BaseModel):
    pbi_id: str
    comment: str


# =========================
# TOOLS
# =========================

@mcp.tool()
def update_pbi_state(input: UpdatePBIStateInput) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pbi_id FROM pbis WHERE pbi_id = ?",
        (input.pbi_id,)
    )
    if not cursor.fetchone():
        conn.close()
        return f"PBI {input.pbi_id} not found"

    cursor.execute(
        "SELECT state_id FROM states WHERE LOWER(name) = LOWER(?)",
        (input.new_state,)
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        return f"State '{input.new_state}' not found"

    state_id = row[0]

    cursor.execute(
        "UPDATE pbis SET state_id = ? WHERE pbi_id = ?",
        (state_id, input.pbi_id)
    )

    conn.commit()
    conn.close()

    return f"{input.pbi_id} moved to {input.new_state}"


@mcp.tool()
def assign_pbi(input: AssignPBIInput) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pbi_id FROM pbis WHERE pbi_id = ?",
        (input.pbi_id,)
    )
    if not cursor.fetchone():
        conn.close()
        return f"PBI {input.pbi_id} not found"

    cursor.execute(
        "SELECT person_id FROM people WHERE LOWER(name) = LOWER(?)",
        (input.person_name,)
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        return f"User '{input.person_name}' not found"

    person_id = row[0]

    cursor.execute(
        "UPDATE pbis SET assigned_to = ? WHERE pbi_id = ?",
        (person_id, input.pbi_id)
    )

    conn.commit()
    conn.close()

    return f"{input.pbi_id} assigned to {input.person_name}"


@mcp.tool()
def add_comment(input: AddCommentInput) -> str:
    from datetime import datetime

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pbi_id FROM pbis WHERE pbi_id = ?",
        (input.pbi_id,)
    )
    if not cursor.fetchone():
        conn.close()
        return f"PBI {input.pbi_id} not found"

    cursor.execute(
        "INSERT INTO comments (pbi_id, comment, created_at) VALUES (?, ?, ?)",
        (input.pbi_id, input.comment, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()

    return f"Comment added to {input.pbi_id}"
