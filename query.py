from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from config import VECTOR_STORE_DIR, EMBED_MODEL_NAME, LLM_MODEL_NAME

import os

def load_vectorstore():
    if not os.path.exists(os.path.join(VECTOR_STORE_DIR, "index.faiss")):
        raise FileNotFoundError("FAISS index not found. Run `ingest.py` first to generate the index.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectordb



def load_qa_chain():
    vectordb = load_vectorstore()
    llm_pipeline = pipeline("text2text-generation", model=LLM_MODEL_NAME)
    llm = HuggingFacePipeline(pipeline=llm_pipeline)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4}),
        return_source_documents=True
    )
    return qa_chain

def ask_question(question: str):
    qa_chain = load_qa_chain()
    result = qa_chain({"query": question})
    return result
