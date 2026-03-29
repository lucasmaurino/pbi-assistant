from agent_graph.state import AgentState
from agent_graph.nodes.kg_node import kg_node


def run_test(question: str):
    state: AgentState = {
        "user_input": question,
        "intent": "informational",
        "kg_result": None,
        "rag_result": None,
        "action": None,
        "action_payload": None,
        "response": None,
        "trace": [],
    }

    new_state = kg_node(state)

    print("User:", question)
    print("KG result:", new_state["kg_result"])
    print("Trace:", new_state["trace"])
    print("-" * 60)


if __name__ == "__main__":
    tests = [
        "Which PBIs belong to Payments Modernization?",
        "What is the status of Payments Modernization?",
        "Who is working on PBI-101?",
        "What PBIs does Alice own?",
        "Which PBIs are active?",
    ]

    for t in tests:
        run_test(t)
