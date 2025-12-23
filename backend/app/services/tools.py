from backend.retriever import query_to_embedding, search_qdrant, format_retrieval_results
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def qdrant_retrieval_tool(query: str, top_k: int = 5) -> str:
    """
    Retrieves relevant document chunks from the Qdrant vector database based on a natural language query.
    
    Args:
        query (str): The natural language query to search for.
        top_k (int): The number of top relevant documents to retrieve.
        
    Returns:
        str: A formatted string containing the retrieved document chunks and their metadata.
    """
    try:
        query_embedding = query_to_embedding(query)
        retrieved_chunks = search_qdrant(query_embedding, top_k=top_k)
        formatted_results = format_retrieval_results(retrieved_chunks)
        logging.info(f"Retrieved content for query '{query}': {formatted_results}")
        return formatted_results
    except Exception as e:
        logging.error(f"Error during Qdrant retrieval tool execution for query '{query}': {e}")
        return f"Error: Could not retrieve information for the query. {e}"

# This is the tool definition that will be exposed to the OpenAI Agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "qdrant_retrieval_tool",
            "description": "Retrieves relevant document chunks from the Qdrant vector database based on a natural language query. Use this tool when you need to find information from the book content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language query to search for in the document chunks."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "The number of top relevant documents to retrieve. Defaults to 5.",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# For local testing of the tool directly
if __name__ == "__main__":
    test_query = "What are the advantages of ROS 2?"
    results = qdrant_retrieval_tool(test_query)
    print("\n--- Test Retrieval Tool Output ---")
    print(results)
