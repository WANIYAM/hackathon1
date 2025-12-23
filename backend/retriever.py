# backend/retriever.py
import os
import cohere
import logging
import time # Import the time module
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not all([QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY]):
    logging.error("Missing one or more environment variables: QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY")
    raise ValueError("Missing one or more environment variables: QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY")

# Initialize Cohere Client
try:
    co = cohere.Client(COHERE_API_KEY)
except cohere.CohereError as e:
    logging.error(f"Failed to initialize Cohere client: {e}")
    raise ValueError(f"Failed to initialize Cohere client: {e}")

# Initialize Qdrant Client (for retrieval)
qdrant_client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)

# Define the Qdrant collection name
COLLECTION_NAME = "rag_embedding"

def query_to_embedding(query: str, model: str = "embed-english-v3.0") -> list[float]:
    """
    Encodes a natural language text query into a Cohere embedding.
    """
    start_time = time.time()
    try:
        response = co.embed(
            texts=[query],
            model=model,
            input_type="search_query" # Use search_query for retrieval tasks
        )
        end_time = time.time()
        logging.info(f"Cohere embedding generation time: {(end_time - start_time) * 1000:.2f} ms")
        return response.embeddings[0]
    except cohere.CohereError as e:
        logging.error(f"Error encoding query with Cohere API: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during query embedding: {e}")
        raise

def search_qdrant(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """
    Queries Qdrant Cloud with a given embedding to retrieve relevant content chunks.
    """
    start_time = time.time()
    try:
        search_result = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            vector=query_embedding,
            limit=top_k,
            with_payload=True # Retrieve the full payload (metadata)
        )
        end_time = time.time()
        logging.info(f"Qdrant similarity search time: {(end_time - start_time) * 1000:.2f} ms")
        
        retrieved_chunks = []
        for hit in search_result:
            chunk = hit.payload
            chunk["score"] = hit.score
            retrieved_chunks.append(chunk)
            
        return retrieved_chunks
    except Exception as e:
        logging.error(f"Error searching Qdrant collection '{COLLECTION_NAME}': {e}")
        raise

def format_retrieval_results(retrieved_chunks: list[dict]) -> str:
    """
    Structures and presents the retrieved chunks, ensuring all required metadata is included.
    """
    if not retrieved_chunks:
        return "No relevant documents found."
    
    formatted_output = []
    for i, chunk in enumerate(retrieved_chunks):
        formatted_output.append(f"--- Result {i+1} (Score: {chunk.get('score', 'N/A'):.4f}) ---")
        formatted_output.append(f"Title: {chunk.get('page_title', 'N/A')}")
        formatted_output.append(f"URL: {chunk.get('source_url', 'N/A')}")
        formatted_output.append(f"Chunk Index: {chunk.get('chunk_index', 'N/A')}")
        formatted_output.append(f"Content Hash: {chunk.get('content_hash', 'N/A')}")
        formatted_output.append(f"Text: \n{chunk.get('chunk_text', 'N/A')}\n")
    
    return "\n".join(formatted_output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("Usage: python retriever.py '<your query text>'")
        sys.exit(1)
    
    query_text = sys.argv[1]
    logging.info(f"Processing query: '{query_text}'")
    
    try:
        # Step 1: Encode query
        query_emb = query_to_embedding(query_text)
        
        # Step 2: Search Qdrant
        results = search_qdrant(query_emb)
        
        # Step 3: Format and print results
        logging.info("\n" + format_retrieval_results(results))
        
    except Exception as e:
        logging.error(f"An error occurred during retrieval: {e}")
