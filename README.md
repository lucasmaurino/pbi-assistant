# 🧠 PBI Assistant

An intelligent assistant for managing and querying Product Backlog Items (PBIs) using a hybrid architecture that combines:

* **Knowledge Graph (structured data)**
* **RAG (Retrieval-Augmented Generation over documents)**
* **Action execution via MCP tools**

---

## 📌 Scope

This assistant is designed for **project management scenarios**, specifically focused on:

### 🔍 Informational Queries

The assistant can answer questions about:

* Feature status and progress
* PBI details (title, state, owner, feature)
* PBIs by:

  * Feature
  * Owner
  * State

It uses:

* **SQLite Knowledge Graph (KG)** → for factual, structured data
* **RAG over documents** → for contextual explanations

---

### ⚡ Actions (Write Operations)

The assistant can modify data through MCP tools:

| Action             | Description                                     |
| ------------------ | ----------------------------------------------- |
| `update_pbi_state` | Move a PBI to a new state                       |
| `assign_pbi`       | Assign a PBI to a person                        |
| `add_comment`      | Add a comment to a PBI *(currently incomplete)* |

---

## 🏗️ Architecture Overview

```
User
 ↓
Intent (LLM)
 ↓
Routing
 ├── Informational → KG → RAG → Synthesis
 └── Action → MCP Tools
```

* **LangGraph** orchestrates the flow
* **LLM (Groq / LLaMA 3.1)** handles:

  * Intent classification
  * Query planning
  * Response synthesis

---

## 📁 Repository Structure

```
agent_graph/
  graph.py
  state.py
  nodes/
    intent.py
    kg_node.py
    rag_node.py
    synthesis.py
    action_node.py

  test_*.py

informational/
  kg/
    db.sqlite
    kg_queries.py
    schema.sql
  rag/
    documents/
    vector_store.py
    loader.py
    build_db.py

mcp_server/
  server.py
  tools.py

scripts/
  init_db.py

ui/
  chat.py
```

---

## ⚙️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Configure environment variables

Create a `.env` file:

```bash
echo GROQ_API_KEY= > .env
```

Then edit `.env` and set your API key:

```bash
GROQ_API_KEY=your_api_key_here
```

You can obtain your API key from the Groq Console.

---

### 3. Initialize the database

```bash
python -m scripts.init_db
```

This will:

* Create the SQLite database
* Load mock data (features, PBIs, users, states)

---

### 4. Build the vector database (RAG)

Run once:

```bash
python -m informational.rag.build_db
```

---

### 5. (Optional) Run MCP server manually

```bash
python -m mcp_server.server
```

⚠️ Not required for normal usage (the client starts it automatically), but needed for:

```bash
python -m agent_graph.test_mcp_client
```

---

## 🚀 Run the Application

```bash
python -m ui.chat
```

Then open:

```
http://127.0.0.1:7860
```

This launches an interactive chat UI using **Gradio**.

---

## 🧪 Testing

You can test each module independently:

### Intent Classification

```bash
python -m agent_graph.test_intent_flow
```

---

### Knowledge Graph Queries

```bash
python -m agent_graph.test_kg_flow
```

---

### RAG Retrieval

```bash
python -m agent_graph.test_rag_flow
```

---

### Synthesis (KG + RAG)

```bash
python -m agent_graph.test_synthesis_flow
```

---

### MCP Client (requires server running)

```bash
python -m mcp_server.server
python -m agent_graph.test_mcp_client
```

---

### Action Execution

```bash
python -m agent_graph.test_action_flow
```

---

### Full End-to-End Flow

```bash
python -m agent_graph.test_full_graph
```

---

## ⚠️ Known Limitations

* `add_comment` MCP tool is not fully implemented
* Telemetry warnings from vector DB libraries may appear (non-blocking)
* Deprecated LangChain classes are used (can be upgraded)

---

## 🧩 Design Principles

* **LLM-driven routing** (no hardcoded logic)
* **Clear separation of concerns**:

  * KG = facts
  * RAG = context
  * MCP = actions
* **Deterministic outputs** (temperature = 0)
* **Composable graph architecture (LangGraph)**

---

## 📈 Possible Improvements

* Complete `add_comment` implementation with persistence
* Replace deprecated LangChain components
* Add authentication / multi-user support
* Improve UI (streaming responses, chat history, debug panel)
* Add validation layer for LLM outputs

---

## 🧠 Summary

This project demonstrates a **production-style AI agent architecture** combining:

* Structured querying (Knowledge Graph)
* Semantic retrieval (RAG)
* Tool execution (MCP)
* Graph-based orchestration (LangGraph)

All exposed through a simple chat interface.

---
