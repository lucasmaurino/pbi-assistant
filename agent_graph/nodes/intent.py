from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

from agent_graph.state import AgentState


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


INTENT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an intent router for a project management agent.

Your only job is to classify the user's request into exactly ONE category:

informational
action

Return ONLY the category name.

----------------------------------

informational:
- asking for status, progress, ownership, details, explanations, analysis

action:
- asking to modify project data (assign, move state, add comment, update)

----------------------------------

Examples:

User: "What is the status of Payments Modernization?"
Answer: informational

User: "Assign PBI-102 to Alice"
Answer: action

User: "Move PBI-101 to Done"
Answer: action

User: "Show me what Bob is working on"
Answer: informational

----------------------------------

Do not explain.
Do not add punctuation.
Return only the word.
"""
    ),
    ("user", "{user_input}")
])


def intent_node(state: AgentState) -> AgentState:
    response = llm.invoke(
        INTENT_PROMPT.format_messages(
            user_input=state["user_input"]
        )
    )

    intent = response.content.strip().lower()

    return {
        **state,
        "intent": intent,
        "trace": state["trace"] + [f"intent={intent}"]
    }
