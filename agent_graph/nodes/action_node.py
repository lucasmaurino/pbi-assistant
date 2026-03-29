import json
import asyncio

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

from agent_graph.state import AgentState

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


ACTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an action planner for a project management system.

Your job is to decide which MCP tool to call and construct the correct input.

Available tools:

1) update_pbi_state
   input: {{ "pbi_id": str, "new_state": str }}

2) assign_pbi
   input: {{ "pbi_id": str, "person_name": str }}

3) add_comment
   input: {{ "pbi_id": str, "comment": str }}

--------------------------------------

Return ONLY a JSON object with this structure:

{{
  "tool": "<tool_name>",
  "input": {{ ... }}
}}

--------------------------------------

Examples:

User: "Move PBI-101 to Done"
→ {{ "tool": "update_pbi_state", "input": {{ "pbi_id": "PBI-101", "new_state": "Done" }} }}

User: "Assign PBI-102 to Alice"
→ {{ "tool": "assign_pbi", "input": {{ "pbi_id": "PBI-102", "person_name": "Alice" }} }}

User: "Add comment to PBI-101 saying testing complete"
→ {{ "tool": "add_comment", "input": {{ "pbi_id": "PBI-101", "comment": "testing complete" }} }}

--------------------------------------

Return only JSON.
"""
    ),
    ("user", "{user_input}")
])


async def call_mcp_tool(tool_name: str, tool_input: dict) -> str:
    server = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"]
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                {"input": tool_input}
            )

            # Extraer texto limpio
            try:
                return result.content[0].text
            except Exception:
                return str(result)


def action_node(state: AgentState) -> AgentState:
    # 1. LLM decide tool + input
    response = llm.invoke(
        ACTION_PROMPT.format_messages(
            user_input=state["user_input"]
        )
    )

    plan = response.content.strip()

    try:
        plan_json = json.loads(plan)
        tool_name = plan_json["tool"]
        tool_input = plan_json["input"]
    except Exception as e:
        raise RuntimeError(f"Action planner failed: {plan}") from e

    # 2. Ejecutar MCP (async dentro de sync)
    result_text = asyncio.run(call_mcp_tool(tool_name, tool_input))

    return {
        **state,
        "response": result_text,
        "trace": state["trace"] + [f"action_tool={tool_name}({tool_input})"]
    }
