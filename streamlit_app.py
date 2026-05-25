# streamlit_app.py

import streamlit as st
import requests

# ← remplace par ton URL ngrok ou garde localhost pour usage local
API_URL = "https://crisped-gap-sanitary.ngrok-free.dev"

st.set_page_config(
    page_title="RailOps Copilot",
    page_icon="🚆",
    layout="centered"
)

st.title("🚆 RailOps Copilot")
st.caption("Assistant IA pour opérateurs ferroviaires SNCF")
st.divider()

mode = st.radio(
    "Mode d'interrogation :",
    ["🤖 Agent complet (LangGraph)", "📋 Procédures uniquement (RAG)"],
    horizontal=True
)

question = st.text_input(
    "Votre question :",
    placeholder="Ex: Y a-t-il des travaux prévus sur la Ligne A ?"
)

if st.button("Envoyer", type="primary") and question:
    with st.spinner("L'agent analyse votre question..."):
        try:
            if "Agent" in mode:
                response = requests.post(f"{API_URL}/agent", json={"question": question})
            else:
                response = requests.post(f"{API_URL}/ask", json={"question": question})

            data = response.json()

            st.success("Réponse :")
            st.markdown(data.get("answer", "Pas de réponse."))

            if "sources" in data and data["sources"]:
                with st.expander("📄 Sources documentaires"):
                    for source in data["sources"]:
                        st.write(f"• {source}")

        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

st.divider()
st.caption("Powered by LangGraph · Ollama · FastAPI · Chroma")