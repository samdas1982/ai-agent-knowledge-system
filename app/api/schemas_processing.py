"""
Extended API schemas for document processing.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Schema for document metadata."""
    
    file_name: str = Field(..., description="Name of the file")
    file_size_bytes: int = Field(..., description="File size in bytes")
    file_extension: str = Field(..., description="File extension")
    created_timestamp: float = Field(..., description="File creation timestamp")
    document_id: Optional[str] = Field(None, description="Unique document ID")
    detected_language: Optional[str] = Field(None, description="Detected language")


class ChunkInfo(BaseModel):
    """Schema for document chunk."""
    
    chunk_id: str = Field(..., description="Unique chunk ID")
    text: str = Field(..., description="Chunk text content")
    length: int = Field(..., description="Length in characters")
    word_count: int = Field(..., description="Number of words")
    position: int = Field(..., description="Position in document")
    total_chunks: int = Field(..., description="Total chunks in document")


class EntityInfo(BaseModel):
    """Schema for extracted entities."""
    
    emails: List[str] = Field(default_factory=list, description="Extracted emails")
    urls: List[str] = Field(default_factory=list, description="Extracted URLs")
    phone_numbers: List[str] = Field(default_factory=list, description="Phone numbers")
    numbers: List[str] = Field(default_factory=list, description="Numbers found")


class IngestionResult(BaseModel):
    """Schema for document ingestion result."""
    
    success: bool = Field(..., description="Ingestion success status")
    document_id: str = Field(..., description="Document ID")
    file_path: str = Field(..., description="Original file path")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    entities: EntityInfo = Field(..., description="Extracted entities")
    chunks: List[ChunkInfo] = Field(..., description="Document chunks")
    chunk_count: int = Field(..., description="Number of chunks")
    total_tokens: int = Field(..., description="Total tokens/words")
    status: str = Field(default="ingested", description="Ingestion status")


class BatchIngestionResult(BaseModel):
    """Schema for batch ingestion result."""
    
    total_documents: int = Field(..., description="Total documents processed")
    successful: int = Field(..., description="Successfully ingested")
    failed: int = Field(..., description="Failed documents")
    documents: List[IngestionResult] = Field(..., description="Ingestion results")
    errors: List[Dict[str, str]] = Field(..., description="Error details")
