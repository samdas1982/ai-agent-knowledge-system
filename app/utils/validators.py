"""
Input validation utilities for the application.
"""

from app.config import get_settings
from app.utils.errors import ValidationError

settings = get_settings()


def validate_file_format(filename: str) -> bool:
    """
    Validate if file format is supported.
    
    Args:
        filename: Name of the file
        
    Returns:
        bool: True if format is supported
        
    Raises:
        ValidationError: If format is not supported
    """
    if not filename:
        raise ValidationError("Filename cannot be empty")

    file_ext = filename.split(".")[-1].lower()

    if file_ext not in settings.supported_formats_list:
        raise ValidationError(
            f"Unsupported file format: {file_ext}. "
            f"Supported formats: {', '.join(settings.supported_formats_list)}"
        )

    return True


def validate_file_size(file_size_bytes: int) -> bool:
    """
    Validate if file size is within limits.
    
    Args:
        file_size_bytes: File size in bytes
        
    Returns:
        bool: True if size is within limits
        
    Raises:
        ValidationError: If file is too large
    """
    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if file_size_bytes > max_size_bytes:
        raise ValidationError(
            f"File size exceeds limit. "
            f"Maximum: {settings.max_upload_size_mb}MB, "
            f"Provided: {file_size_bytes / (1024 * 1024):.2f}MB"
        )

    return True


def validate_query(query: str) -> bool:
    """
    Validate user query.
    
    Args:
        query: User's natural language query
        
    Returns:
        bool: True if query is valid
        
    Raises:
        ValidationError: If query is invalid
    """
    if not query:
        raise ValidationError("Query cannot be empty")

    if len(query) < 3:
        raise ValidationError("Query must be at least 3 characters long")

    if len(query) > 5000:
        raise ValidationError("Query cannot exceed 5000 characters")

    return True


def validate_chunk_parameters(chunk_size: int, chunk_overlap: int) -> bool:
    """
    Validate document chunking parameters.
    
    Args:
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        bool: True if parameters are valid
        
    Raises:
        ValidationError: If parameters are invalid
    """
    if chunk_size <= 0:
        raise ValidationError("Chunk size must be positive")

    if chunk_overlap < 0:
        raise ValidationError("Chunk overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValidationError("Chunk overlap must be less than chunk size")

    return True
