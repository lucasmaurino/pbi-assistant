from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENTS_PATH = Path(__file__).parent / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.md"):
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()
        documents.extend(docs)

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def load_and_split():
    docs = load_documents()
    return split_documents(docs)
