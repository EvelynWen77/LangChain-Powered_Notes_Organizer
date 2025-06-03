from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

def build_faiss_index(documents):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(documents, embeddings)

def save_faiss_index(vectorstore, save_path="./data/faiss_index"):
    vectorstore.save_local(save_path)

def load_faiss_index(save_path="./data/faiss_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True  
    )
