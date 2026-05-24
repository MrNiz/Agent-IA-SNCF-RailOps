# app/ingestion/loaders.py
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path("data/docs")


def load_raw_docs():
    docs = []

    # Markdown et texte brut
    for ext in ("*.md", "*.txt"):
        for path in DOCS_DIR.rglob(ext):
            loader = TextLoader(str(path), encoding="utf-8")
            docs.extend(loader.load())

    # PDF
    for path in DOCS_DIR.rglob("*.pdf"):
        loader = PyPDFLoader(str(path))
        docs.extend(loader.load())

    # plus tard: HTML, DOCX, etc.

    return docs


def load_and_split_docs():
    raw_docs = load_raw_docs()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    split_docs = splitter.split_documents(raw_docs)
    return split_docs