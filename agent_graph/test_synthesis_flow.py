from agent_graph.nodes.synthesis import synthesis_node
from agent_graph.state import AgentState


def run_test(question, kg_result, rag_result):
    state: AgentState = {
        "user_input": question,
        "intent": "informational",
        "kg_result": kg_result,
        "rag_result": rag_result,
        "action": None,
        "action_payload": None,
        "response": None,
        "trace": []
    }

    new_state = synthesis_node(state)

    print("User:", question)
    print("Answer:")
    print(new_state["response"])
    print("Trace:", new_state["trace"])
    print("-" * 60)


if __name__ == "__main__":

    run_test(
        "What is the status of Payments Modernization?",
        {"Active": 1, "New": 1},
        "Payments Modernization aims to modernize legacy ETL pipelines and improve reliability."
    )

    run_test(
        "What does PBI-102 focus on?",
        {
            "pbi_id": "PBI-102",
            "title": "Refactor validation rules",
            "feature": "Payments Modernization",
            "assigned_to": "Bob",
            "state": "New"
        },
        "This PBI focuses on centralizing validation logic and improving data quality checks."
    )
