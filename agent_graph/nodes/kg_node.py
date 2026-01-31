from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from agent_graph.state import AgentState
from informational.kg.kg_queries import (
    get_pbis_by_feature,
    get_pbis_by_person,
    get_pbis_by_state,
    get_feature_progress,
    get_pbi_details,
)

from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


KG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a structured data query planner for a project knowledge graph.

Your job is to decide which structured query to run and with what parameter.

Available functions:

1) get_pbis_by_feature(feature_name)
2) get_pbis_by_person(person_name)
3) get_pbis_by_state(state_name)
4) get_feature_progress(feature_name)
5) get_pbi_details(pbi_id)

--------------------------------------

Return a JSON object with exactly:

{{
  "tool": "<function_name>",
  "argument": "<single string argument>"
}}

--------------------------------------

Examples:

User: "What is the status of Payments Modernization?"
→ {{"tool": "get_feature_progress", "argument": "Payments Modernization"}}

User: "Who is working on PBI-101?"
→ {{"tool": "get_pbi_details", "argument": "PBI-101"}}

User: "What PBIs does Alice own?"
→ {{"tool": "get_pbis_by_person", "argument": "Alice"}}

User: "Which PBIs are active?"
→ {{"tool": "get_pbis_by_state", "argument": "Active"}}

User: "Which PBIs belong to Payments Modernization?"
→ {{"tool": "get_pbis_by_feature", "argument": "Payments Modernization"}}

--------------------------------------

Return only JSON.
"""
    ),
    ("user", "{user_input}")
])


KG_FUNCTIONS = {
    "get_pbis_by_feature": get_pbis_by_feature,
    "get_pbis_by_person": get_pbis_by_person,
    "get_pbis_by_state": get_pbis_by_state,
    "get_feature_progress": get_feature_progress,
    "get_pbi_details": get_pbi_details,
}


def kg_node(state: AgentState) -> AgentState:
    response = llm.invoke(
        KG_PROMPT.format_messages(
            user_input=state["user_input"]
        )
    )

    plan = response.content.strip()

    try:
        import json
        plan_json = json.loads(plan)
        tool_name = plan_json["tool"]
        argument = plan_json["argument"]
    except Exception as e:
        raise RuntimeError(f"KG planner failed: {plan}") from e

    if tool_name not in KG_FUNCTIONS:
        raise RuntimeError(f"Unknown KG tool: {tool_name}")

    result = KG_FUNCTIONS[tool_name](argument)

    return {
        **state,
        "kg_result": result,
        "trace": state["trace"] + [f"kg_tool={tool_name}({argument})"]
    }
