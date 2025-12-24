import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.agent import RAGAgent
from backend.app.services.tools import qdrant_retrieval_tool

# Mock settings for testing
@pytest.fixture(autouse=True)
def mock_settings():
    with patch('backend.app.core.config.get_settings') as mock_get_settings:
        mock_settings_instance = MagicMock()
        mock_settings_instance.OPENAI_API_KEY = "mock_openai_key"
        mock_get_settings.return_value = mock_settings_instance
        yield

@pytest.fixture
def rag_agent_instance():
    # Patch ChatOpenAI during RAGAgent initialization
    with patch('langchain_openai.ChatOpenAI'), \
         patch('langchain.agents.create_tool_calling_agent'), \
         patch('langchain.agents.AgentExecutor'):
        agent = RAGAgent()
        # Mock the ask_question method's internal LLM and agent_executor
        agent.llm = MagicMock()
        agent.agent_executor = MagicMock()
        yield agent

def test_ask_question_with_context_snippet(rag_agent_instance):
    """
    Test that the agent prioritizes context_snippet if provided.
    """
    query = "What is the capital of France?"
    context = "Paris is the capital of France."
    expected_response = "Paris is the capital of France."

    rag_agent_instance.llm.invoke.return_value.content = expected_response

    response = rag_agent_instance.ask_question(query, context_snippet=context)
    assert response == expected_response
    rag_agent_instance.llm.invoke.assert_called_once()
    rag_agent_instance.agent_executor.invoke.assert_not_called()

def test_ask_question_without_context_snippet_invokes_tool(rag_agent_instance):
    """
    Test that the agent uses the retrieval tool if no context_snippet is provided.
    """
    query = "What is Docusaurus?"
    retrieval_tool_response = "Docusaurus is a static site generator."
    agent_executor_response = {"output": retrieval_tool_response}

    rag_agent_instance.agent_executor.invoke.return_value = agent_executor_response

    response = rag_agent_instance.ask_question(query)
    assert response == retrieval_tool_response
    rag_agent_instance.agent_executor.invoke.assert_called_once_with({
        "input": query, 
        "chat_history": []
    })
    rag_agent_instance.llm.invoke.assert_not_called() # Should not call direct LLM when tool is used

def test_ask_question_error_handling(rag_agent_instance):
    """
    Test error handling in ask_question method.
    """
    query = "Test error"
    rag_agent_instance.agent_executor.invoke.side_effect = Exception("Agent error")

    response = rag_agent_instance.ask_question(query)
    assert "An error occurred while processing your request." in response
    rag_agent_instance.agent_executor.invoke.assert_called_once()
