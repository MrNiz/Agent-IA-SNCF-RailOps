# tests/test_app.py

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.fastapi_app import app
from app.db.sqlite_db import run_query

client = TestClient(app)


# --- Mock LLM pour éviter d'appeler Ollama (non dispo en CI) ---

FAKE_LLM_RESPONSE = "Voici les étapes de gestion d'un incident de niveau 1."

@pytest.fixture(autouse=True)
def mock_ollama():
    """Remplace l'appel Ollama par une réponse simulée dans tous les tests."""
    with patch("app.rag.chains.ChatOllama") as mock_llm_class:
        mock_llm = MagicMock()
        mock_llm_class.return_value = mock_llm
        mock_llm.invoke.return_value = MagicMock(content=FAKE_LLM_RESPONSE)

        # Mock pour RetrievalQA chain
        with patch("app.rag.chains.RetrievalQA") as mock_qa:
            mock_chain = MagicMock()
            mock_qa.from_chain_type.return_value = mock_chain
            mock_chain.invoke.return_value = {
                "result": FAKE_LLM_RESPONSE,
                "source_documents": [
                    MagicMock(metadata={"source": "procedure_gestion_incident_niveau1.md"})
                ]
            }
            yield


# --- Tests API ---

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer():
    response = client.post("/ask", json={"question": "Quelles sont les étapes de gestion d'un incident ?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 5


def test_ask_returns_sources():
    response = client.post("/ask", json={"question": "procédure incident niveau 1"})
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert isinstance(data["sources"], list)


# --- Tests SQL ---

def test_run_query_incidents():
    rows = run_query("SELECT COUNT(*) FROM incidents")
    assert rows[0][0] >= 3


def test_run_query_travaux():
    rows = run_query("SELECT COUNT(*) FROM travaux")
    assert rows[0][0] >= 3


def test_run_query_invalid_table():
    with pytest.raises(Exception):
        run_query("SELECT * FROM table_inexistante")