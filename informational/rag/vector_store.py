from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from .loader import load_and_split


VECTOR_DB_PATH = Path(__file__).parent / "chroma_db"


def build_vector_store():
    documents = load_and_split()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_PATH)
    )

    return vector_store


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embeddings
    )


def search(query: str, k: int = 3):
    store = load_vector_store()
    return store.similarity_search(query, k=k)
