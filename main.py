# main.py - Put everything together in the main.py file to orchestrate the flow from ingestion to querying
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from backend.extract_text import extract_text_from_pdf
from backend.embedding_generation import generate_embeddings
from backend.vector_store import setup_vector_store
from backend.rag_chain import build_rag_chain

# Step 1: Load the PDF and extract text
pdf_path = "data/daikin.pdf"
manual_text = extract_text_from_pdf(pdf_path)

# Step 2: Generate embeddings
text_chunks, embeddings = generate_embeddings(manual_text)

# Step 3: Set up vector store
faiss_index = setup_vector_store(embeddings)

# Step 4: Set up RAG chain (retriever + LLM)
rag_chain = build_rag_chain(faiss_index, text_chunks)

# Step 5: Query the chatbot
while True:
    query = input("Ask a question about the product manual (type 'exit' to quit): ")
    
    if query.lower() == 'exit':
        print("Exiting...")
        break
    
    # Get the answer using the RAG chain
    response = rag_chain.invoke(query)

    print(f"Answer: {response}")
