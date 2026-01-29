from typing import Literal

from agent_graph.state import AgentState


def route_from_intent(state: AgentState) -> Literal["kg_path", "action_path"]:
    """
    LangGraph routing function.

    This does NOT perform reasoning.
    It only routes based on the LLM-produced intent value.

    Allowed outputs must match graph edge keys.
    """

    intent = state["intent"]

    if intent == "action":
        return "action_path"

    # default informational path
    return "kg_path"
