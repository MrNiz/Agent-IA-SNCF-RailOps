# app/agent.py

from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from app.tools.rag_tool import search_documentation
from app.tools.analytics import run_incident_query, search_travaux


def get_agent():
    """
    Agent RailOps Copilot :
    - search_documentation : recherche dans les procédures (RAG)
    - run_incident_query   : requêtes analytiques sur la base incidents (SQL)
    - search_travaux       : travaux planifiés/en cours sur les lignes (SQL)
    """
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.1,
    )

    tools = [search_documentation, run_incident_query, search_travaux]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es RailOps Copilot, un assistant intelligent pour les opérateurs ferroviaires SNCF.
Tu as accès à trois outils :
- search_documentation : pour répondre à des questions sur les procédures opérationnelles.
- run_incident_query   : pour exécuter des requêtes SQL sur la base des incidents.
- search_travaux       : pour consulter les travaux planifiés, en cours ou terminés sur les lignes.
Utilise toujours l'outil le plus adapté à la question. Réponds en français."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
    )