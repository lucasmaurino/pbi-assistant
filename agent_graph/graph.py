from langgraph.graph import StateGraph, END
from agent_graph.state import AgentState

from agent_graph.nodes.intent import intent_node
from agent_graph.nodes.kg_node import kg_node
from agent_graph.nodes.rag_node import rag_node
from agent_graph.nodes.synthesis import synthesis_node


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("intent_classifier", intent_node)
    graph.add_node("kg_query", kg_node)
    graph.add_node("rag_search", rag_node)
    graph.add_node("synthesis_step", synthesis_node)

    # Entry
    graph.set_entry_point("intent_classifier")

    # LLM-driven routing (NO manual if/else)
    graph.add_conditional_edges(
        "intent_classifier",
        lambda state: state["intent"],
        {
            "informational": "kg_query",
            "action": END
        }
    )

    # Informational pipeline
    graph.add_edge("kg_query", "rag_search")
    graph.add_edge("rag_search", "synthesis_step")
    graph.add_edge("synthesis_step", END)

    return graph.compile()
