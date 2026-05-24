# app/tools/analytics.py

from langchain_core.tools import tool
from app.db.sqlite_db import run_query


@tool
def run_incident_query(query: str) -> str:
    """
    Exécute une requête SQL en lecture sur la table incidents (SQLite).
    Renvoie les résultats sous forme de texte.
    À utiliser par un agent pour répondre à des questions analytiques.
    """
    try:
        rows = run_query(query)
    except Exception as e:
        return f"Erreur SQL : {e}"

    if not rows:
        return "Aucun résultat."

    return "\n".join(" | ".join(str(v) for v in row) for row in rows)


@tool
def search_travaux(query: str) -> str:
    """
    Exécute une requête SQL sur la table travaux (SQLite).
    À utiliser pour répondre aux questions sur les travaux planifiés,
    en cours ou nécessaires sur les lignes ferroviaires.
    """
    try:
        rows = run_query(query)
    except Exception as e:
        return f"Erreur SQL : {e}"

    if not rows:
        return "Aucun travail trouvé."

    return "\n".join(" | ".join(str(v) for v in row) for row in rows)