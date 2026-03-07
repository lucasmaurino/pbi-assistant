from agent_graph.state import AgentState
from agent_graph.nodes.intent import intent_node
from agent_graph.nodes.decision import route_from_intent


def run_test(user_input: str):
    state: AgentState = {
        "user_input": user_input,
        "intent": None,
        "kg_result": None,
        "rag_result": None,
        "action": None,
        "action_payload": None,
        "response": None,
        "trace": []
    }

    state = intent_node(state)
    route = route_from_intent(state)

    print("\nUser:", user_input)
    print("Intent:", state["intent"])
    print("Route:", route)
    print("Trace:", state["trace"])
    print("-" * 50)


if __name__ == "__main__":
    tests = [
        "What is the status of Payments Modernization?",
        "Assign PBI-102 to Alice",
        "Move PBI-101 to Done",
        "Show me what Bob is working on",
        "Add a comment to PBI-101 saying testing is complete",
        "How much progress do we have on Payments Modernization?",
        "Who owns PBI-101?"
    ]

    for t in tests:
        run_test(t)
