# Quickstart Guide: RAG Agent Service

This guide provides instructions on how to set up the environment and run the RAG Agent Service, which is a FastAPI application.

## Prerequisites

Before you begin, ensure you have the following:

-   **Python 3.11+**: Installed on your system.
-   **`uv`**: A fast Python package installer and resolver.
-   **Qdrant Cloud Account**: Access to a Qdrant Cloud instance. The `rag_embedding` collection should be populated (from Spec 1).
-   **OpenAI API Key**: For the OpenAI Agents SDK.
-   **Cohere API Key**: For query embeddings by the retrieval tool.
-   **Environment Variables**: Set the following environment variables (preferably in a `.env` file in the project root):
    -   `QDRANT_HOST`: Your Qdrant Cloud instance URL (e.g., `https://<your-cluster-id>.qdrant.tech`)
    -   `QDRANT_API_KEY`: Your Qdrant Cloud API key
    -   `COHERE_API_KEY`: Your Cohere API key (used by the retrieval tool)
    -   `OPENAI_API_KEY`: Your OpenAI API key

## Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Activate your virtual environment (if not already active)**:
    ```bash
    .\.venv\Scripts\activate  # On Windows
    # source .venv/bin/activate  # On Linux/macOS
    ```

3.  **Install/Update dependencies using `uv` or `pip`**:
    ```bash
    uv pip install -r requirements.txt
    # or
    pip install -r requirements.txt
    ```

## Running the FastAPI Service

To start the RAG Agent Service:

```bash
uvicorn app.main:app --reload
```

The service will typically run on `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Testing the API Endpoint

You can interact with the agent via the `/chat` endpoint.

**Example using `curl`**:

```bash
curl -X POST "http://127.00.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d 
     {
       "query_text": "What are the benefits of using Isaac ROS VSLAM?",
       "context_snippet": ""
     }

```

**Example with context snippet**:

```bash
curl -X POST "http://127.00.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d 
     {
       "query_text": "What is the key advantage of this framework?",
       "context_snippet": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints."
     }

```

## Verification

-   Send queries to the `/chat` endpoint and verify that the agent responds accurately based on retrieved or provided context.
-   Check the response headers for latency metrics to ensure NFR-002 is met.
-   Review service logs for any errors or unexpected behavior.
