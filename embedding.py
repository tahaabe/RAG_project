from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config import OLLAMA_EMBED_MODEL, VECTORDB_DIR
import json, os


def embed_and_store(chunks_dir="chunks", persist_directory=VECTORDB_DIR, batch_size=16):
    embedder = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
    documents = []
    for fn in os.listdir(chunks_dir):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(chunks_dir, fn), "r", encoding="utf8") as f:
            items = json.load(f)
        for it in items:
            documents.append(Document(
                page_content=it["page_content"],
                metadata=it.get("metadata", {})
            ))
    if not documents:
        raise ValueError(f"No chunk JSON files found in {chunks_dir!r}. Run ingest.py first.")
    print(f"Embedding {len(documents)} chunks into {persist_directory}")
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedder,
    )
    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]
        vectordb.add_documents(batch)
        print(f"Embedded {min(start + batch_size, len(documents))}/{len(documents)} chunks")
    return vectordb


if __name__ == "__main__":
    embed_and_store()
