from agent_graph.graph import build_graph
from agent_graph.state import AgentState


def run_test(message: str):
    graph = build_graph()

    state: AgentState = {
        "user_input": message,
        "intent": None,
        "kg_result": None,
        "rag_result": None,
        "action": None,
        "action_payload": None,
        "response": None,
        "trace": []
    }

    result = graph.invoke(state)

    print("User:", message)
    print("Answer:")
    print(result["response"])
    print("Trace:", result["trace"])
    print("-" * 60)


if __name__ == "__main__":
    tests = [
        # Feature level
        "What is the status of Payments Modernization?",
        "Which PBIs belong to the Payments Modernization feature?",

        # PBI details
        "What does PBI-102 focus on?",
        "Can you give me details about PBI-101?",

        # By state
        "Which PBIs are currently In Progress?",
        "Which PBIs are already Done?",

        # By person (si tenés datos cargados)
        "Which PBIs is Alice working on?",
        "Which PBIs are assigned to Bob?"
    ]

    for q in tests:
        run_test(q)
        print("-" * 60)

