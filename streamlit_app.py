import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


import streamlit as st
from ingest import ingest
from query import ask_question
import os
from config import DATA_DIR

st.set_page_config(page_title="📚 Research Assistant", layout="wide")

st.title("📚 Research Paper Assistant")
st.markdown("Upload academic PDFs and ask natural language questions using RAG.")

# Upload PDFs
st.header("1. Upload PDF Documents")
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_path = os.path.join(DATA_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
    st.success(f"Uploaded {len(uploaded_files)} files.")

# Ingest PDFs
if st.button("📥 Ingest & Embed Documents"):
    with st.spinner("Processing PDFs..."):
        ingest()
    st.success("Documents embedded and stored successfully!")

# Ask a Question
st.header("2. Ask a Question")
query = st.text_input("Enter your question (e.g., 'What is greenwashing?')")

if st.button("🔍 Get Answer") and query:
    with st.spinner("Searching and generating answer..."):
        result = ask_question(query)
        st.markdown(f"### 🧠 Answer\n{result['result']}")

        st.markdown("### 📄 Source Excerpts")
        for doc in result["source_documents"]:
            with st.expander(doc.metadata["source"]):
                st.write(doc.page_content)
