from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from config import VECTOR_STORE_DIR, EMBED_MODEL_NAME, LLM_MODEL_NAME

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = FAISS.load_local(VECTOR_STORE_DIR, embeddings)
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
    print(f"\nAnswer: {result['result']}\n")
    print("Sources:")
    for doc in result['source_documents']:
        print(f"- {doc.metadata['source']}: {doc.page_content[:200]}...\n")
