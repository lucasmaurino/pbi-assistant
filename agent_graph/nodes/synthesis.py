from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from agent_graph.state import AgentState

from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a project intelligence assistant.

You receive:

1) Structured project data from a Knowledge Graph (KG)
2) Contextual background from documents (RAG)

Your job is to synthesize them into a clear, concise answer.

Rules:

- Use KG data as the source of truth for status, ownership, progress
- Use RAG data for explanations, goals, and background
- Do NOT dump raw data
- Summarize and connect insights
- Be concise and professional
"""
    ),
    (
        "user",
        """
User question:
{question}

Structured data (KG):
{kg_result}

Contextual data (RAG):
{rag_result}

Provide a synthesized answer.
"""
    )
])


def synthesis_node(state: AgentState) -> AgentState:
    response = llm.invoke(
        SYNTHESIS_PROMPT.format_messages(
            question=state["user_input"],
            kg_result=state["kg_result"],
            rag_result=state["rag_result"],
        )
    )

    answer = response.content.strip()

    return {
        **state,
        "response": answer,
        "trace": state["trace"] + ["synthesis"]
    }
