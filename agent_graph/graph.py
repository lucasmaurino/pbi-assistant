from langgraph.graph import StateGraph, END
from agent_graph.state import AgentState

from agent_graph.nodes.intent import intent_node
from agent_graph.nodes.kg_node import kg_node
from agent_graph.nodes.rag_node import rag_node
from agent_graph.nodes.synthesis import synthesis_node
from agent_graph.nodes.action_node import action_node


def build_graph():
    graph = StateGraph(AgentState)

    # =========================
    # Nodes
    # =========================
    graph.add_node("intent_classifier", intent_node)
    graph.add_node("kg_query", kg_node)
    graph.add_node("rag_search", rag_node)
    graph.add_node("synthesis_step", synthesis_node)
    graph.add_node("action_executor", action_node)

    # =========================
    # Entry
    # =========================
    graph.set_entry_point("intent_classifier")

    # =========================
    # Routing (LLM-driven)
    # =========================
    graph.add_conditional_edges(
        "intent_classifier",
        lambda state: state["intent"],
        {
            "informational": "kg_query",
            "action": "action_executor"
        }
    )

    # =========================
    # Informational pipeline
    # =========================
    graph.add_edge("kg_query", "rag_search")
    graph.add_edge("rag_search", "synthesis_step")
    graph.add_edge("synthesis_step", END)

    # =========================
    # Action pipeline
    # =========================
    graph.add_edge("action_executor", END)

    return graph.compile()
