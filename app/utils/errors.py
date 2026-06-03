"""
Custom exception classes for the application.
"""


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, error_code: str = "APP_ERROR"):
        """
        Initialize error.
        
        Args:
            message: Error message
            error_code: Error code for categorization
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DocumentProcessingError(AppError):
    """Raised when document processing fails."""

    def __init__(self, message: str):
        super().__init__(message, "DOCUMENT_PROCESSING_ERROR")


class EmbeddingError(AppError):
    """Raised when embedding generation fails."""

    def __init__(self, message: str):
        super().__init__(message, "EMBEDDING_ERROR")


class RetrievalError(AppError):
    """Raised when document retrieval fails."""

    def __init__(self, message: str):
        super().__init__(message, "RETRIEVAL_ERROR")


class LLMError(AppError):
    """Raised when LLM call fails."""

    def __init__(self, message: str):
        super().__init__(message, "LLM_ERROR")


class AgentError(AppError):
    """Raised when agent execution fails."""

    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class VectorDBError(AppError):
    """Raised when vector database operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "VECTOR_DB_ERROR")
