# backend/vector_store. - Store embeddings in a vector database for efficient retrieval
import faiss
import numpy as np

def setup_vector_store(embeddings):
    embedding_size = len(embeddings[0])  # Get embedding size (384 for MiniLM)
    
    # Initialize FAISS index
    index = faiss.IndexFlatL2(embedding_size)
    
    # Add embeddings to the index
    index.add(np.array(embeddings))
    
    return index

