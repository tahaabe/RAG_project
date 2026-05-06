from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import OLLAMA_CHAT_MODEL, OLLAMA_EMBED_MODEL, VECTORDB_DIR

app = FastAPI()

# Load vector DB and set up retriever
embedding_fn = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
vectordb = Chroma(persist_directory=VECTORDB_DIR, embedding_function=embedding_fn)
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# LLM
llm = ChatOllama(model=OLLAMA_CHAT_MODEL, temperature=0.0)
prompt = PromptTemplate.from_template(
    "Use the following context to answer the question. "
    "If the answer is not in the context, say 'I don't know.'\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

class QueryIn(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "ok", "ask_endpoint": "/ask", "model": OLLAMA_CHAT_MODEL}

@app.post("/ask")
def ask(q: QueryIn):
    try:
        result = qa.invoke({"query": q.question})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result.get("source_documents", [])]
    }
