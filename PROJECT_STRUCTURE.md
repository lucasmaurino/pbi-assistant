# Estructura del Proyecto - PBI Assistant

```
pbi-assistant/
│
├── agent_graph/                 # 👈 LangGraph - Núcleo del sistema
│   ├── state.py                 # Define el estado del agente (AgentState)
│   ├── nodes/
│   │   ├── intent.py            # Nodo de clasificación de intención (informational/action)
│   │   ├── kg_node.py           # Nodo de consulta a Knowledge Graph
│   │   ├── rag_node.py          # Nodo de búsqueda RAG
│   │   └── decision.py          # Nodo de decisión de enrutamiento
│   │
│   └── test_*.py                # Tests para cada flujo
│       ├── test_intent_flow.py
│       ├── test_kg_flow.py
│       └── test_rag_flow.py
│
├── informational/               # 👈 Fuentes de información
│   ├── kg/                      # Knowledge Graph (hechos estructurados)
│   │   ├── kg_queries.py        # Funciones de consulta a KG
│   │   └── schema.sql           # Esquema de la base de datos
│   │
│   └── rag/                     # RAG (contexto y explicaciones)
│       ├── loader.py            # Cargador de documentos
│       ├── vector_store.py      # Gestión de vector store (Chroma)
│       ├── build_db.py          # Script de construcción de BD vectorial
│       └── documents/           # Documentos de referencia
│           ├── backlog_guidelines.md
│           ├── feature_payments.md
│           ├── pbi_101_description.md
│           └── pbi_102_description.md
│
├── mcp_server/                  # 👈 Servidor MCP (proceso separado)
│   └── (archivos en construcción)
│
├── ui/                          # 👈 Interfaz de usuario
│   └── (archivos en construcción)
│
├── scripts/                     # 👈 Scripts de inicialización
│   └── init_db.py               # Script de inicialización de BD (KG)
│
├── requirements.txt             # Dependencias del proyecto
└── .gitignore                   # Archivos a excluir de versionamiento

EXCLUIDOS (versionamiento):
- venv/                          # Virtual environment
- __pycache__/                   # Cache de Python
- *.pyc                          # Bytecode compilado
- .env                           # Variables de entorno secretas
- chroma_db/                     # Base de datos vectorial (generada)

ARCHIVOS SIN CONTENIDO (NO INCLUIDOS):
- agent_graph/__init__.py
- agent_graph/graph.py
- agent_graph/nodes/__init__.py
- agent_graph/nodes/synthesis.py
- informational/kg/__init__.py
- informational/rag/__init__.py
- mcp_server/schemas.py
- mcp_server/server.py
- mcp_server/tools.py
- ui/chat.py
- README.md
```

## Flujo Principal

```
Usuario
   ↓
[Intent Node] → clasifica intención (informational/action)
   ↓
   ├─→ Si ACTION → MCP Client (confirmación)
   │
   └─→ Si INFORMATION
        ↓
        [KG Node] → hechos estructurados
        ↓
        [RAG Node] → contexto y explicaciones
        ↓
        [Synthesis Node] → combina información inteligentemente
        ↓
        Final Answer
```
