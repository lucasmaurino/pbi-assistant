import sqlite3
from pathlib import Path
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP


DB_PATH = Path(__file__).parents[1] / "informational" / "kg" / "db.sqlite"

mcp = FastMCP("pbi-action-server")


class UpdatePBIStateInput(BaseModel):
    pbi_id: str
    new_state: str


@mcp.tool()
def update_pbi_state(input: UpdatePBIStateInput) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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

    return f"PBI {input.pbi_id} moved to {input.new_state}"
