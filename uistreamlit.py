import streamlit as st
import requests

st.title("RAG demo - IPCC AR6 (Ollama + LangChain)")

q = st.text_input("Ask a question about the IPCC reports")

if st.button("Ask") and q:
    resp = requests.post("http://localhost:8000/ask", json={"question": q})
    if resp.ok:
        data = resp.json()
        st.subheader("Answer")
        st.write(data["answer"])
        st.subheader("Sources")
        for source in data["sources"]:
            st.write(source)
    else:
        st.error("API error: " + str(resp.status_code))
