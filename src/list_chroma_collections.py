import chromadb
from chromadb.config import Settings

if __name__ == "__main__":
    client = chromadb.PersistentClient(
        path="vector_store/chromadb_sample_dataset",
        settings=Settings(anonymized_telemetry=False, allow_reset=True)
    )
    collections = client.list_collections()
    print("Available ChromaDB collections:")
    for col in collections:
        print(f"- {col.name}") 