import gradio as gr

from agent_graph.graph import build_graph
from agent_graph.state import AgentState


graph = build_graph()


def chat(user_input, history):
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

    result = graph.invoke(state)

    return result["response"]


demo = gr.ChatInterface(
    fn=chat,
    title="PBI Assistant",
    description="Ask about PBIs, features, or perform actions"
)


if __name__ == "__main__":
    demo.launch()
