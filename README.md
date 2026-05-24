# RailOps Copilot — Agent IA pour opérateurs ferroviaires

> **Assistant intelligent SNCF** combinant RAG, LangGraph, agent multi-tools et API REST — entièrement local, zéro cloud, déployable via Docker.

![CI](https://github.com/MrNiz/Agent-IA-SNCF-RailOps/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

## But du projet

RailOps Copilot permet à un opérateur ferroviaire d'**interroger en langage naturel les données ferroviaires** :

- Les **procédures opérationnelles** (gestion d'incidents, protocoles sécurité)
- La **base de données incidents** (statistiques, historique par ligne)
- Les **travaux planifiés ou en cours** sur les lignes

**Exemple de flux complet :**
Question : "Y a-t-il des travaux prévus sur la Ligne A ?"
↓
[router_node] → détecte "travaux"
↓
[travaux_node] → SQL : SELECT * FROM travaux WHERE ligne = 'Ligne A'
↓
[llm_node] → Ollama reformule la réponse
↓
"Des travaux de remplacement d'aiguillage sont prévus du 1er au 3 juin..."


---

## Architecture
```          
┌──────────────────────────┐
│ FastAPI REST API         │
│ /health /ask /agent      │
└────────────┬─────────────┘
             │
┌────────────▼─────────────────────┐
│ LangGraph StateGraph             │
│ [router_node]                    │
│ (routage conditionnel)           │
└──────┬──────── ── ┬───────────┬──┘
       │            │           │
┌──────▼──────┐ ┌───▼──┐ ┌──────▼──────┐
│ rag_node    │ │ sql  │ │travaux_node │
│ Chroma DB   │ │ node │ │ SQLite DB   │
│ HuggingFace │ │      │ │             │
└──────┬──────┘ └──┬───┘ └────┬────────┘
       │           │          │
┌──────▼───────────▼──────────▼────────┐
│ [llm_node]                           │
│ Ollama qwen2.5:3b                    │
└──────────────────────────────────────┘
```          

## Stack technique

| Composant | Technologie |
|---|---|
| API | FastAPI + Uvicorn |
| LLM local | Ollama `qwen2.5:3b` |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| VectorDB | Chroma |
| Base de données | SQLite |
| Agent & Orchestration | LangGraph `StateGraph` |
| RAG | LangChain / LangChain-Classic |
| Tests | pytest + httpx |
| Lint | Ruff |
| CI/CD | GitHub Actions |
| Containerisation | Docker |

---

## Run

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

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/health` | Statut de l'API |
| `POST` | `/ask` | RAG pur — question sur les procédures |
| `POST` | `/agent` | Agent LangGraph multi-tools (RAG + SQL incidents + travaux) |

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


---

## Docker

```bash
docker build -t railops-copilot .
docker run -p 8000:8000 railops-copilot
```

---

## Structure du projet

| Chemin | Description |
|---|---|
| `app/agent.py` | LangGraph StateGraph + routage conditionnel |
| `app/fastapi_app.py` | Routes FastAPI `/health` `/ask` `/agent` |
| `app/db/sqlite_db.py` | Connexion SQLite + `run_query` |
| `app/rag/chains.py` | Chaîne RetrievalQA |
| `app/rag/vectorstore.py` | Chroma + HuggingFace embeddings |
| `app/tools/analytics.py` | Tools SQL : incidents + travaux |
| `app/tools/rag_tool.py` | Tool RAG : `search_documentation` |
| `data/docs/` | Procédures opérationnelles `.md` |
| `scripts/init_db.py` | Création + seed base SQLite |
| `scripts/ingest_docs.py` | Indexation docs → VectorStore |
| `tests/test_app.py` | Tests pytest (6 tests) |
| `.github/workflows/ci.yml` | Pipeline CI : lint + test + docker build |
| `Dockerfile` | Image Docker de l'API |

---

## Auteur

**Nizar Alioua** — Data Engineer & IA  
[LinkedIn](https://linkedin.com/in/nizar-alioua) · [GitHub](https://github.com/MrNiz)
