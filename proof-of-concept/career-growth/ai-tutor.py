import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain  
from langchain_classic.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Load Qwen Model 
def load_llm():
    llm = ChatGroq(
        groq_api_key=os.getenv("career-growth"),
        model="qwen2.5-72b-instruct",
        temperature=0.2
    )
    return llm

# Load textbook and create Vector DB
def build_vector_db(pdf_path="./books/Hands-On-Machine-Learning.pdf"):
    print("Loading textbook...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("Creating embeddings...")
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Building FAISS vector database....")
    vectordb = FAISS.from_documents(chunks, embedding)
    return vectordb.as_retriever(search_type="similarity", k=4)


# Build RAG Tutor Chain
def build_tutor_chain(llm, retriever):
    prompt = PromptTemplate.from_template(
    """
    You are an AI Tutor teaching IT concepts clearly and simply.
    Use ONLY the provided context from the textbook.
                                          
    Question: {input}
    
    CONTEXT:
    {context}

    Your response must include:
    - Beginner-level explanation
    - Real-world analogy or example
    - 3-step learning plan
    - A short quiz with answers
    """
    )

    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain


# Tutor Ask Function
def ask_tutor(chain, question):

    print("\nStudent Question: {question}")
    response = chain.invoke({"input": question})
    print("\n Tutor Response: \n")
    print(response["answer"])
    return response["answer"]


if __name__ == "__main__":
    llm = load_llm()
    retriever = build_vector_db()
    tutor_chain = build_tutor_chain(llm, retriever)

    rslt = ask_tutor(
        tutor_chain,
        "Explain about cybersecurity."
    )