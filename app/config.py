"""
Configuration management for the AI Agent Knowledge System.
Loads settings from environment variables using Pydantic.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Settings
    app_name: str = "AI Agent Knowledge System"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_title: str = "AI Agent Knowledge System API"
    api_version: str = "1.0.0"

    # LLM Configuration
    openai_api_key: str
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000

    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # Vector Database Configuration
    vector_db_type: str = "faiss"
    vector_db_path: str = "./vector_store"
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "ai-knowledge-index"

    # Document Processing
    max_upload_size_mb: int = 50
    chunk_size: int = 1000
    chunk_overlap: int = 200
    supported_formats: str = "pdf,txt,csv,xlsx,docx,json,yaml"

    # Retrieval Configuration
    top_k_retrieval: int = 5
    similarity_threshold: float = 0.5

    # Agent Configuration
    agent_type: str = "react"
    agent_timeout: int = 300
    max_iterations: int = 10

    # Security
    secret_key: str = "your-secret-key-here"
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # Storage Paths
    upload_dir: str = "./uploaded_documents"
    processed_dir: str = "./processed_data"
    log_dir: str = "./logs"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def supported_formats_list(self) -> list[str]:
        """Return supported formats as a list."""
        return [fmt.strip().lower() for fmt in self.supported_formats.split(",")]

    @property
    def allowed_origins_list(self) -> list[str]:
        """Return allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    def validate_paths(self) -> None:
        """Create necessary directories if they don't exist."""
        for path in [self.upload_dir, self.processed_dir, self.log_dir, self.vector_db_path]:
            os.makedirs(path, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    settings = Settings()
    settings.validate_paths()
    return settings


# For backward compatibility
settings = get_settings()
