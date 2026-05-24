from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

PERSIST_DIR = "data/vectorstore"

load_dotenv()


def get_embeddings():
    """
    Utilise un modèle d'embeddings gratuit en local.
    Aucun besoin de clé OpenAI.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vectorstore(documents):
    """
    Construit et persiste un vectorstore Chroma à partir des documents.
    """
    embeddings = get_embeddings()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )

    vectordb.persist()
    return vectordb


def load_vectorstore():
    """
    Charge un vectorstore Chroma déjà construit.
    """
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )

    return vectordb