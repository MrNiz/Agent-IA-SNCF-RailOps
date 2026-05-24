from app.ingestion.loaders import load_and_split_docs
from app.rag.vectorstore import build_vectorstore


def main():
    docs = load_and_split_docs()
    print(f"Nombre de documents après split : {len(docs)}")
    build_vectorstore(docs)
    print("Vectorstore construit et persisté dans data/vectorstore.")


if __name__ == "__main__":
    main()