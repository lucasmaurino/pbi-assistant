from agent_graph.nodes.action_node import action_node


def run_test(user_input: str):
    state = {
        "user_input": user_input,
        "intent": "action",
        "kg_result": None,
        "rag_result": None,
        "action": None,
        "action_payload": None,
        "response": None,
        "trace": []
    }

    result = action_node(state)

    print(f"User: {user_input}")
    print("Response:", result["response"])
    print("Trace:", result["trace"])
    print("-" * 60)


if __name__ == "__main__":
    run_test("Move PBI-101 to Done")
    run_test("Assign PBI-102 to Bob")
    run_test("Add comment to PBI-101 saying testing completed")
