# tests/test_app.py

import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import app
from app.db.sqlite_db import run_query

client = TestClient(app)


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
    assert len(data["answer"]) > 10


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