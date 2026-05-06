import os
from pathlib import Path


VECTORDB_DIR = os.environ.get(
    "RAG_VECTORDB_DIR",
    str(Path.home() / ".rag_vectordb"),
)
OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.1")
OLLAMA_EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text:latest")
