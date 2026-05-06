# RAG Demo - IPCC AR6

This project is a local Retrieval-Augmented Generation demo for asking questions about IPCC AR6 PDF reports.

It uses:

- FastAPI for the `/ask` backend API
- Streamlit for the browser UI
- LangChain for loading, splitting, retrieval, and QA
- Chroma as the local vector database
- Ollama for local embeddings and chat models

## Requirements

- Python 3.9+
- Ollama installed and running
- An Ollama embedding model:

```powershell
ollama pull nomic-embed-text
```

- A small chat model, for example:

```powershell
ollama pull llama3.2:1b
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Put your PDF files in the `data/` folder.

## Build the Vector Database

First split the PDFs into chunks:

```powershell
python ingest.py
```

Then embed the chunks into Chroma:

```powershell
python embedding.py
```

By default, the Chroma database is stored outside the OneDrive project folder at:

```text
C:\Users\<your-user>\.rag_vectordb
```

You can override that location:

```powershell
$env:RAG_VECTORDB_DIR="C:\path\to\vectordb"
```

## Run the App

Start the FastAPI backend:

```powershell
$env:OLLAMA_CHAT_MODEL="llama3.2:1b"
uvicorn app:app --reload
```

Open a second PowerShell window and start Streamlit:

```powershell
streamlit run uistreamlit.py
```

Then open:

```text
http://localhost:8501
```

## API

Health check:

```text
GET http://localhost:8000/
```

Ask a question:

```text
POST http://localhost:8000/ask
```

Example request body:

```json
{
  "question": "By how much has global surface temperature increased since the pre-industrial period?"
}
```

## Notes

- `chunks/`, `vectordb/`, `.venv/`, and local SQLite files are ignored by Git.
- If Ollama returns a memory error, use a smaller model such as `llama3.2:1b`.
