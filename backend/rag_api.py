from flask import Flask, request, jsonify
from extract_text import extract_text_from_pdf
from embedding_generation import generate_embeddings
from vector_store import setup_vector_store
from rag_chain import build_rag_chain
import os

app = Flask(__name__)

# Add a print statement to indicate the app has started
print("Starting Flask RAG API...")

# Load environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Step 1: Load the PDF and extract text
pdf_path = "data/daikin.pdf"
print(f"Loading PDF from: {pdf_path}")
manual_text = extract_text_from_pdf(pdf_path)

# Step 2: Generate embeddings
print("Generating embeddings...")
text_chunks, embeddings = generate_embeddings(manual_text)

# Step 3: Set up vector store
print("Setting up vector store...")
faiss_index = setup_vector_store(embeddings)

# Step 4: Set up RAG chain (retriever + LLM)
print("Building RAG chain...")
rag_chain = build_rag_chain(faiss_index, text_chunks)

@app.route('/api/rag', methods=['POST'])
def get_rag_response():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Run the RAG pipeline with the user message
        response = rag_chain.run(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Only for local development
if __name__ == '__main__':
    # Get port from environment variables (use Heroku's port when deployed)
    port = int(os.environ.get('PORT', 5001))  # Default to 5001 for local development
    app.run(host='0.0.0.0', port=port, debug=True)

