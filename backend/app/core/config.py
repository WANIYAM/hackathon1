from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    OPENAI_API_KEY: str
    QDRANT_HOST: str
    QDRANT_API_KEY: str
    COHERE_API_KEY: str

    APP_NAME: str = "RAGAgentService"
    DEBUG_MODE: bool = False
    
    # Qdrant settings for retrieval
    QDRANT_COLLECTION_NAME: str = "rag_embedding"
    QDRANT_VECTOR_SIZE: int = 1024 # Based on Cohere embed-english-v3.0
    
    # Cohere settings
    COHERE_EMBED_MODEL: str = "embed-english-v3.0"

@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings class.
    """
    return Settings()

