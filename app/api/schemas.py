"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# Document Schemas
class DocumentBase(BaseModel):
    """Base document schema."""

    name: str = Field(..., description="Document name")
    content_type: str = Field(..., description="MIME type of document")


class DocumentUpload(DocumentBase):
    """Schema for document upload."""

    pass


class DocumentInfo(DocumentBase):
    """Schema for document information response."""

    id: str = Field(..., description="Unique document ID")
    size_bytes: int = Field(..., description="Document size in bytes")
    chunks_count: int = Field(default=0, description="Number of chunks")
    uploaded_at: datetime = Field(..., description="Upload timestamp")
    status: str = Field(default="processed", description="Processing status")


class DocumentListResponse(BaseModel):
    """Schema for document list response."""

    documents: List[DocumentInfo]
    total_count: int


# Query Schemas
class QueryRequest(BaseModel):
    """Schema for query request."""

    question: str = Field(..., description="Natural language question", min_length=3, max_length=5000)
    top_k: int = Field(default=5, ge=1, le=20, description="Number of documents to retrieve")
    include_sources: bool = Field(default=True, description="Include source references in response")
    conversation_id: Optional[str] = Field(None, description="For multi-turn conversations")


class SourceDocument(BaseModel):
    """Schema for source document reference."""

    document_id: str = Field(..., description="ID of source document")
    document_name: str = Field(..., description="Name of source document")
    chunk_id: str = Field(..., description="ID of specific chunk")
    content: str = Field(..., description="Relevant chunk content")
    similarity_score: float = Field(..., description="Similarity score (0-1)")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class QueryResponse(BaseModel):
    """Schema for query response."""

    response: str = Field(..., description="Generated response to the query")
    confidence: float = Field(..., description="Confidence score (0-1)")
    sources: Optional[List[SourceDocument]] = Field(None, description="Source documents used")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    model_used: str = Field(..., description="LLM model used")
    agent_reasoning: Optional[str] = Field(None, description="Agent reasoning steps")


class ConversationMessage(BaseModel):
    """Schema for conversation message."""

    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationResponse(BaseModel):
    """Schema for conversation response."""

    conversation_id: str
    messages: List[ConversationMessage]
    latest_response: QueryResponse


# Health Check Schema
class HealthResponse(BaseModel):
    """Schema for health check response."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    environment: str = Field(..., description="Environment (dev/prod)")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Error Schema
class ErrorResponse(BaseModel):
    """Schema for error response."""

    detail: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    error_type: str = Field(..., description="Exception type")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Status Schema
class StatusResponse(BaseModel):
    """Schema for system status response."""

    status: str = Field(..., description="System status")
    vector_db_connected: bool = Field(..., description="Vector DB connection status")
    llm_available: bool = Field(..., description="LLM availability")
    documents_count: int = Field(..., description="Number of documents")
    total_chunks: int = Field(..., description="Total document chunks")
    embeddings_cached: int = Field(..., description="Number of cached embeddings")
