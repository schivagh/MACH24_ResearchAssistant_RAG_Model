import os
from config import DATA_DIR, VECTOR_STORE_DIR, EMBED_MODEL_NAME
from utils import extract_text_from_pdf
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs():
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            text = extract_text_from_pdf(path)
            docs.append((file, text))
    return docs

def ingest():
    documents = load_pdfs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = []
    metadata = []

    for fname, doc in documents:
        for chunk in splitter.split_text(doc):
            texts.append(chunk)
            metadata.append({"source": fname})

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadata)
    vectordb.save_local(VECTOR_STORE_DIR)

if __name__ == "__main__":
    ingest()
