# app/agent.py

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

from app.tools.rag_tool import search_documentation
from app.tools.analytics import run_incident_query, search_travaux


# --- 1. Définition de l'état du graphe ---

class AgentState(TypedDict):
    question: str
    tool_used: str
    tool_result: str
    answer: str


# --- 2. Les nodes ---

def router_node(state: AgentState) -> AgentState:
    """Décide quel tool appeler selon la question."""
    question = state["question"].lower()

    if any(w in question for w in ["travaux", "chantier", "maintenance", "réfection", "planifié"]):
        return {**state, "tool_used": "travaux"}
    elif any(w in question for w in ["incident", "panne", "combien", "statistique", "ligne", "count"]):
        return {**state, "tool_used": "incidents"}
    else:
        return {**state, "tool_used": "rag"}


def rag_node(state: AgentState) -> AgentState:
    """Cherche dans les procédures documentaires."""
    result = search_documentation.invoke(state["question"])
    return {**state, "tool_result": result}


def incidents_node(state: AgentState) -> AgentState:
    """Interroge la base incidents en SQL."""
    # Construit une requête SQL simple selon la question
    question = state["question"].lower()
    if "combien" in question or "count" in question:
        if "ligne a" in question:
            query = "SELECT COUNT(*) FROM incidents WHERE ligne = 'Ligne A'"
        else:
            query = "SELECT ligne, COUNT(*) as nb FROM incidents GROUP BY ligne"
    else:
        query = "SELECT * FROM incidents LIMIT 5"

    result = run_incident_query.invoke(query)
    return {**state, "tool_result": result}


def travaux_node(state: AgentState) -> AgentState:
    """Interroge la base travaux en SQL."""
    question = state["question"].lower()
    if "ligne a" in question:
        query = "SELECT * FROM travaux WHERE ligne = 'Ligne A'"
    elif "en cours" in question:
        query = "SELECT * FROM travaux WHERE statut = 'en cours'"
    elif "prévu" in question:
        query = "SELECT * FROM travaux WHERE statut = 'prévu'"
    else:
        query = "SELECT * FROM travaux"

    result = search_travaux.invoke(query)
    return {**state, "tool_result": result}


def llm_node(state: AgentState) -> AgentState:
    """Reformule la réponse finale avec le LLM."""
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.1)

    prompt = f"""Tu es RailOps Copilot, assistant intelligent pour les opérateurs ferroviaires SNCF.

Question : {state['question']}

Données disponibles :
{state['tool_result']}

Réponds en français de manière claire et structurée en te basant sur les données ci-dessus."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "answer": response.content}


# --- 3. Condition de routage ---

def route_to_tool(state: AgentState) -> Literal["rag_node", "incidents_node", "travaux_node"]:
    mapping = {
        "rag":      "rag_node",
        "incidents": "incidents_node",
        "travaux":  "travaux_node",
    }
    return mapping[state["tool_used"]]


# --- 4. Construction du graphe ---

def build_graph():
    graph = StateGraph(AgentState)

    # Ajout des nodes
    graph.add_node("router_node",   router_node)
    graph.add_node("rag_node",      rag_node)
    graph.add_node("incidents_node", incidents_node)
    graph.add_node("travaux_node",  travaux_node)
    graph.add_node("llm_node",      llm_node)

    # Point d'entrée
    graph.set_entry_point("router_node")

    # Routage conditionnel
    graph.add_conditional_edges("router_node", route_to_tool)

    # Tous les tools → llm_node → END
    graph.add_edge("rag_node",       "llm_node")
    graph.add_edge("incidents_node", "llm_node")
    graph.add_edge("travaux_node",   "llm_node")
    graph.add_edge("llm_node",       END)

    return graph.compile()


# --- 5. Fonction publique appelée par FastAPI ---

def get_agent():
    return build_graph()