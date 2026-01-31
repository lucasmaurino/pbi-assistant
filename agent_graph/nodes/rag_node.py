from agent_graph.state import AgentState
from informational.rag.vector_store import search


def rag_node(state: AgentState) -> AgentState:
    docs = search(state["user_input"], k=3)

    combined_context = "\n".join(d.page_content for d in docs)

    return {
        **state,
        "rag_result": combined_context,
        "trace": state["trace"] + ["rag_search"]
    }
