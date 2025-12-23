from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.app.services.tools import qdrant_retrieval_tool, tools as agent_tools
from backend.app.core.config import get_settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

settings = get_settings()

class RAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o", # Or a suitable model like "gpt-3.5-turbo"
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Use the provided tools to answer questions about the book content. "
                    "If a question cannot be answered using the tools, state that you cannot find the information."
                    "Always cite your sources by mentioning the URL from the retrieved content.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.agent = create_tool_calling_agent(self.llm, agent_tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=agent_tools, verbose=True)

    def ask_question(self, query: str, context_snippet: str = None, chat_history: list = None) -> str:
        """
        Asks the RAG agent a question and returns its answer.
        Prioritizes context_snippet if provided.
        """
        try:
            if chat_history is None:
                chat_history = []
            
            if context_snippet:
                # If context is provided, instruct the LLM to use it directly
                # We bypass the agent executor with tools here for direct LLM call
                logging.info("Context snippet provided. Prioritizing context for LLM response.")
                direct_prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            f"You are a helpful assistant. Answer the following question ONLY based on the provided context. "
                            f"Context: {context_snippet}\n\n"
                            "If the answer cannot be found in the context, state that the information is not in the provided context.",
                        ),
                        MessagesPlaceholder(variable_name="chat_history"),
                        ("human", "{input}"),
                    ]
                )
                direct_llm_chain = direct_prompt | self.llm
                response = direct_llm_chain.invoke({
                    "input": query, 
                    "chat_history": chat_history
                })
                return response.content # Langchain's invoke returns an AIMessage object
            else:
                # If no context snippet, use the agent with tools for retrieval
                logging.info("No context snippet provided. Using RAG agent with retrieval tool.")
                response = self.agent_executor.invoke({
                    "input": query, 
                    "chat_history": chat_history # Integrate chat history if needed for conversation
                })
                return response["output"]
        except Exception as e:
            logging.error(f"Error asking question to agent: {e}")
            return "An error occurred while processing your request."


rag_agent = RAGAgent()

if __name__ == "__main__":
    # Example usage for testing the agent directly
    test_query = "What are the benefits of using Isaac ROS VSLAM?"
    response = rag_agent.ask_question(test_query)
    logging.info(f"Agent Response for '{test_query}': {response}")

    test_query_2 = "Tell me about Docusaurus."
    response_2 = rag_agent.ask_question(test_query_2)
    logging.info(f"Agent Response for '{test_query_2}': {response_2}")
