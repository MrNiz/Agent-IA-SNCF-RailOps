# app/fastapi_app.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.chains import get_rag_chain
from app.agent import get_agent

app = FastAPI(title="RailOps Copilot API")


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(payload: Question):
    chain = get_rag_chain()
    result = chain.invoke({"query": payload.question})
    sources = list(dict.fromkeys(
        doc.metadata.get("source", "")
        for doc in result["source_documents"]
        if doc.metadata.get("source")
    ))
    return {"answer": result["result"], "sources": sources}


@app.post("/agent")
def agent_ask(payload: Question):
    """
    Endpoint agent : combine RAG docs + SQL incidents.
    L'agent choisit lui-même le bon outil selon la question.
    """
    agent = get_agent()
    result = agent.invoke({"input": payload.question})
    return {"answer": result["output"]}