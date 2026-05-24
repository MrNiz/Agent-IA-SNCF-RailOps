# app/tools/rag_tool.py

from langchain_core.tools import tool
from app.rag.vectorstore import load_vectorstore


@tool
def search_documentation(question: str) -> str:
    """
    Recherche dans la documentation procédurale SNCF (procédures, guides, règles).
    À utiliser pour répondre à des questions sur les procédures opérationnelles.
    """
    vectordb = load_vectorstore()
    docs = vectordb.similarity_search(question, k=3)

    if not docs:
        return "Aucun document pertinent trouvé."

    results = []
    for i, doc in enumerate(docs, 1):
        results.append(f"[Doc {i}] {doc.page_content}")

    return "\n\n".join(results)