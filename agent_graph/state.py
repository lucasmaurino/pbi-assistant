from typing import TypedDict, Optional, Any, List, Literal, Union


class AgentState(TypedDict):
    # raw user input
    user_input: str

    # routing decision (LLM decides — no manual logic)
    intent: Optional[Literal["informational", "action"]]

    # ===== Informational flow =====
    kg_result: Optional[Union[dict, list]]  # structured data from KG
    rag_result: Optional[str]               # unstructured context from RAG

    # ===== Action flow =====
    action: Optional[str]           # tool name to execute
    action_payload: Optional[dict]  # arguments for the tool

    # ===== Final output =====
    response: Optional[str]

    # ===== Debug trace (dev only, not user-facing) =====
    trace: List[str]
