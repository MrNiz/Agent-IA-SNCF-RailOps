# RailOps Copilot — Agent IA pour opérateurs ferroviaires

> **Assistant intelligent SNCF** combinant RAG, agent multi-tools et API REST — déployable via Docker.

![CI](https://github.com/MrNiz/Agent-IA-SNCF-RailOps/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

---

## But du projet

RailOps Copilot permet à un opérateur ferroviaire d'**interroger en langage naturel les données ferroviaires de l'entreprise** :
- Les **procédures opérationnelles** (gestion d'incidents, protocoles sécurité)
- La **base de données incidents** (statistiques, historique par ligne)
- Les **travaux planifiés ou en cours** sur les lignes

"Quelles sont les étapes de gestion d'un incident niveau 1 ?"
↓
Agent LangChain → sélectionne le bon tool
↓
RAG  → recherche dans les procédures
↓
LLM Ollama → génère la réponse
↓
"1. Qualifier l'incident... 2. Vérifier les conditions de sécurité..."



## Architecture
┌─────────────────────────────────────────────────────┐
│ FastAPI (REST API)                                  │
│ /health /ask /agent                                 │
└──────────────┬──────────────┬───────────────────────┘

┌──────▼──────┐ ┌─────────────▼──────────┐
│ RAG Chain   │ │     Agent LangChain    │
│AgentExecutor│ │                        │
│ Chroma DB │ │ │
│ + HuggingF. │ │ ┌─────────────────────┐│
│ Embeddings  │ │ │ search_documentation││
└─────────────┘ │ │ run_incident_query  ││
│                 │ search_travaux      ││
│                 └─────────────────────┘│
└────────────┬────────────┘
     ┌───────▼──────┐
     │ SQLite DB    │
     │ incidents    │
     │ travaux      │
     └──────────────┘

## Stack

| Composant       |           Technologie           |
|-----------------|---------------------------------|
| API             | FastAPI + Uvicorn               |
| LLM local       | Ollama `qwen2.5:3b`             |
| Embeddings      | HuggingFace `all-MiniLM-L6-v2`  |
| VectorDB        | Chroma                          |
| Base de données | SQLite                          |
| Agent & RAG     | LangChain / LangChain-Classic   |
| Tests           | pytest + httpx                  |
| Lint            | Ruff                            |
| CI/CD           | GitHub Actions                  |
| Containerisation| Docker                          |

---

## Run le projet localement

### Prérequis
- Python 3.12+
- [Ollama](https://ollama.com) installé avec le modèle `qwen2.5:3b`

```bash
ollama pull qwen2.5:3b
```

### Installation

```bash
# 1. Cloner le repo
git clone https://github.com/MrNiz/Agent-IA-SNCF-RailOps.git
cd Agent-IA-SNCF-RailOps

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base SQLite (incidents + travaux)
python -m scripts.init_db

# 5. Indexer les documents dans le VectorStore
python -m scripts.ingest_docs

# 6. Lancer l'API
uvicorn app.fastapi_app:app --reload
```

L'API est accessible sur **http://localhost:8000/docs** (Swagger UI).

---

## Endpoints

| Méthode | Route    | Description                                       |
|---------|----------|---------------------------------------------------|
| `GET`   | `/health`| Statut de l'API                                   |
| `POST`  | `/ask`   | RAG pur — question sur les procédures             |
| `POST`  | `/agent` | Agent multi-tools (RAG + SQL incidents + travaux) |

### Exemple `/ask`
```json
POST /ask
{
  "question": "Quelles sont les étapes de gestion d'un incident niveau 1 ?"
}
```

### Exemple `/agent`
```json
POST /agent
{
  "question": "Y a-t-il des travaux prévus sur la Ligne A ?"
}
```

---

## Tests

```bash
python -m pytest tests/ -v
```
tests/test_app.py::test_health PASSED
tests/test_app.py::test_ask_returns_answer PASSED
tests/test_app.py::test_ask_returns_sources PASSED
tests/test_app.py::test_run_query_incidents PASSED
tests/test_app.py::test_run_query_travaux PASSED
tests/test_app.py::test_run_query_invalid_table PASSED

6 passed in 31s


## Docker

```bash
docker build -t railops-copilot .
docker run -p 8000:8000 railops-copilot
```

---

## Structure du projet
Agent-IA-SNCF-RailOps/
├── app/
│ ├── agent.py # AgentExecutor LangChain + 3 tools
│ ├── fastapi_app.py # Routes FastAPI (/health, /ask, /agent)
│ ├── db/
│ │ └── sqlite_db.py # Connexion SQLite + run_query
│ ├── rag/
│ │ ├── chains.py # Chaîne RetrievalQA
│ │ └── vectorstore.py # Chroma + embeddings
│ └── tools/
│ ├── analytics.py # Tools SQL : incidents + travaux
│ └── rag_tool.py # Tool RAG : search_documentation
├── data/
│ └── docs/ # Procédures opérationnelles (.md)
├── scripts/
│ ├── init_db.py # Création + seed SQLite
│ └── ingest_docs.py # Indexation docs → VectorStore
├── tests/
│ └── test_app.py # Tests pytest (6 tests)
├── .github/
│ └── workflows/
│ └── ci.yml # Pipeline CI (lint + test + docker)
├── Dockerfile
└── requirements.txt

## Auteur

**Nizar Alioua** — Data Engineer & IA  
[LinkedIn](https://linkedin.com/in/nizar-alioua) · [GitHub](https://github.com/MrNiz)