import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, patch
from backend.app.main import app
from backend.app.models import AgentQuery, AgentResponse

# Mock settings for testing
@pytest.fixture(autouse=True)
def mock_settings():
    with patch('backend.app.core.config.get_settings') as mock_get_settings:
        mock_settings_instance = MagicMock()
        mock_settings_instance.OPENAI_API_KEY = "mock_openai_key"
        mock_settings_instance.QDRANT_HOST = "mock_qdrant_host"
        mock_settings_instance.QDRANT_API_KEY = "mock_qdrant_key"
        mock_settings_instance.COHERE_API_KEY = "mock_cohere_key"
        mock_get_settings.return_value = mock_settings_instance
        yield

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_read_root(async_client: AsyncClient):
    """
    Test the root endpoint.
    """
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RAG Agent Service is running!"}

@pytest.mark.asyncio
async def test_chat_general_query(async_client: AsyncClient):
    """
    Test the /chat endpoint with a general query (without context_snippet).
    """
    query_text = "What is Docusaurus?"
    expected_response_text = "Docusaurus is a static site generator for building documentation websites."
    
    with patch('backend.app.services.agent.rag_agent.ask_question') as mock_ask_question:
        mock_ask_question.return_value = expected_response_text
        
        response = await async_client.post(
            "/chat",
            json={"query_text": query_text, "context_snippet": None}
        )
        
        assert response.status_code == 200
        response_data = AgentResponse(**response.json())
        assert response_data.response_text == expected_response_text
        assert mock_ask_question.called_once_with(query=query_text, context_snippet=None)
        assert response_data.source_references == []
        assert response_data.used_context == None

@pytest.mark.asyncio
async def test_chat_context_limited_query(async_client: AsyncClient):
    """
    Test the /chat endpoint with a context-limited query.
    """
    query_text = "What are the key features?"
    context_snippet = "FastAPI is a modern, fast (high-performance) web framework."
    expected_response_text = "Based on the provided context, the key features are that it's a modern, fast, high-performance web framework."

    with patch('backend.app.services.agent.rag_agent.ask_question') as mock_ask_question:
        mock_ask_question.return_value = expected_response_text
        
        response = await async_client.post(
            "/chat",
            json={"query_text": query_text, "context_snippet": context_snippet}
        )
        
        assert response.status_code == 200
        response_data = AgentResponse(**response.json())
        assert response_data.response_text == expected_response_text
        assert mock_ask_question.called_once_with(query=query_text, context_snippet=context_snippet)
        assert response_data.used_context == context_snippet

@pytest.mark.asyncio
async def test_chat_missing_query_text(async_client: AsyncClient):
    """
    Test /chat endpoint with missing query_text.
    """
    response = await async_client.post(
        "/chat",
        json={"query_text": None, "context_snippet": "some context"}
    )
    
    assert response.status_code == 422 # Pydantic validation error

@pytest.mark.asyncio
async def test_chat_agent_error(async_client: AsyncClient):
    """
    Test error handling when the agent encounters an error.
    """
    query_text = "Trigger agent error"
    with patch('backend.app.services.agent.rag_agent.ask_question') as mock_ask_question:
        mock_ask_question.side_effect = Exception("Internal agent error")
        
        response = await async_client.post(
            "/chat",
            json={"query_text": query_text, "context_snippet": None}
        )
        
        assert response.status_code == 500
        assert "An internal server error occurred." in response.json()["detail"]
