# backend/embedding_generation.py - Break text into smaller chunks and generate embeddings

from sentence_transformers import SentenceTransformer

def generate_embeddings(text):
    # Load the model for generating embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Split the document into chunks
    text_chunks = [text[i:i + 500] for i in range(0, len(text), 500)]  # Split every 500 characters

    # Generate embeddings for each chunk
    embeddings = model.encode(text_chunks)
    
    return text_chunks, embeddings
