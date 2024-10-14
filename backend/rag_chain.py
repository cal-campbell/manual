# backend/rag_chain.py - Combine the retriever (which will query the vector store) and the language model (which will generate responses based on the retrieved content)
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer  # Use SentenceTransformer directly
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAI
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# Load environment variables from .env file
load_dotenv()

def build_rag_chain(faiss_index, text_chunks):
    # Create documents from the text chunks
    documents = [Document(page_content=chunk) for chunk in text_chunks]
    
    # Initialize an in-memory docstore
    docstore = InMemoryDocstore({i: doc for i, doc in enumerate(documents)})
    
    # Create a mapping from FAISS index to document IDs
    index_to_docstore_id = {i: i for i in range(len(text_chunks))}
    
    # Load the SentenceTransformers embedding model directly
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize the FAISS vectorstore with the embedding model's encode method
    vectorstore = FAISS(embedding_function=embedding_model.encode, 
                        index=faiss_index, 
                        docstore=docstore, 
                        index_to_docstore_id=index_to_docstore_id)

    # Initialize the OpenAI LLM using the correct import
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    
    return qa_chain

