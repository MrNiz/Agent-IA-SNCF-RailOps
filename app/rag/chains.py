# app/rag/chains.py

from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_classic.chains import RetrievalQA

from app.rag.vectorstore import load_vectorstore


# Charge les variables d'environnement depuis le fichier .env
load_dotenv()


def get_llm():
    """
    Initialise le LLM local avec Ollama.
    Aucun appel API externe : gratuit, local, sans clé OpenAI/HuggingFace.
    """

    llm = ChatOllama(
        model="qwen2.5:0.5b",
        temperature=0.1,
        num_predict=512,
    )

    return llm


def get_rag_chain():
    """
    Construit une chaîne RAG :
    - charge le vectorstore Chroma
    - récupère les documents pertinents
    - envoie le contexte au LLM local Ollama
    """

    vectordb = load_vectorstore()

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = get_llm()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
    )

    return chain