from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from backend.app.core.config import get_settings
from backend.app.models import AgentQuery, AgentResponse
from backend.app.services.agent import rag_agent
import logging
import time # Import the time module
from openai import OpenAIError # For specific OpenAI exceptions
from cohere import CohereError # For specific Cohere exceptions
from qdrant_client.http.exceptions import UnexpectedResponse # For specific Qdrant exceptions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG_MODE,
    version="1.0.0",
    description="API for interacting with the RAG Agent Service.",
)

@app.get("/")
async def read_root():
    return {"message": "RAG Agent Service is running!"}

# --- Exception Handlers ---
@app.exception_handler(OpenAIError)
async def openai_exception_handler(request: Request, exc: OpenAIError):
    logging.error(f"OpenAI API error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY, # Bad Gateway for external API errors
        content={"detail": f"OpenAI API error: {exc.message}"},
    )

@app.exception_handler(CohereError)
async def cohere_exception_handler(request: Request, exc: CohereError):
    logging.error(f"Cohere API error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": f"Cohere API error: {exc.message}"},
    )

@app.exception_handler(UnexpectedResponse)
async def qdrant_exception_handler(request: Request, exc: UnexpectedResponse):
    logging.error(f"Qdrant API error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": f"Qdrant API error: {exc.content}"},
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logging.error(f"Application ValueError: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"An unhandled error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )
# --- End Exception Handlers ---

@app.post("/query", response_model=AgentResponse)
async def query_rag_agent(query_request: AgentQuery):
    """
    Endpoint to query the RAG Agent.
    """
    start_time = time.time() # Start latency measurement
    try:
        agent_response_text = rag_agent.ask_question(
            query=query_request.query,
            context_snippet=query_request.context # Pass the context
        )
        
        # In a more advanced scenario, source_references and used_context
        # would be extracted from the agent's full response or tool outputs.
        # For now, we'll return a placeholder or infer from the response.
        return AgentResponse(
            response_text=agent_response_text,
            source_references=[], # To be filled more intelligently later
            used_context=query_request.context # Reflect the used context
        )
    finally:
        end_time = time.time() # End latency measurement
        duration = (end_time - start_time) * 1000 # Convert to milliseconds
        logging.info(f"Query endpoint response time for query '{query_request.query}': {duration:.2f} ms")
        # For p95, a more advanced metric collection system (e.g., Prometheus, custom list) would be needed.
