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
1) Structured data from a Knowledge Graph (KG)
2) Contextual background from documents (RAG)

Your job is to combine them into a clear and useful answer.

Rules:

- Always prioritize KG for factual data (status, ownership, counts)
- Use RAG to enrich the answer with context, explanations, or purpose
- If KG has no results:
    → Say it clearly
    → Still use RAG to provide helpful context if available
- Do NOT mention "KG" or "RAG" in the answer
- Do NOT artificially separate sources
- Do NOT invent data not present in KG
- Keep answers concise but informative

- NEVER mix information from different PBIs or features if the question is about a specific one
- NEVER infer data not present in KG
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
