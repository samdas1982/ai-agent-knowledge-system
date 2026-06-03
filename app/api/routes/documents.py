"""
Document management endpoints.
Handles document upload, listing, retrieval, and deletion.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
import os
import uuid
from datetime import datetime
from pathlib import Path

from app.config import get_settings
from app.utils.logger import setup_logger
from app.utils.validators import validate_file_format, validate_file_size
from app.utils.errors import ValidationError, DocumentProcessingError
from app.api.schemas import DocumentInfo, DocumentListResponse, ErrorResponse

logger = setup_logger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/documents", tags=["Documents"])

# In-memory storage for demo (will be replaced with database in later tasks)
documents_db = {}


@router.post("/upload", response_model=DocumentInfo, status_code=201)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing.
    
    Supported formats: PDF, TXT, CSV, XLSX, DOCX, JSON, YAML
    Max file size: 50MB
    
    Args:
        file: The document file to upload
        
    Returns:
        DocumentInfo: Information about the uploaded document
        
    Raises:
        HTTPException: If file format is not supported or file is too large
    """
    try:
        # Validate file format
        logger.info(f"Processing file upload: {file.filename}")
        validate_file_format(file.filename)
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        validate_file_size(file_size)
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Save file to upload directory
        file_path = os.path.join(settings.upload_dir, f"{doc_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Store document metadata
        doc_info = {
            "id": doc_id,
            "name": file.filename,
            "content_type": file.content_type or "application/octet-stream",
            "size_bytes": file_size,
            "chunks_count": 0,
            "uploaded_at": datetime.utcnow(),
            "status": "uploaded",
            "file_path": file_path,
        }
        
        documents_db[doc_id] = doc_info
        
        logger.info(f"Document uploaded successfully: {doc_id} ({file.filename})")
        
        return DocumentInfo(
            id=doc_id,
            name=file.filename,
            content_type=file.content_type or "application/octet-stream",
            size_bytes=file_size,
            chunks_count=0,
            uploaded_at=datetime.utcnow(),
            status="uploaded",
        )
        
    except ValidationError as e:
        logger.warning(f"Validation error during upload: {e.message}")
        raise HTTPException(
            status_code=400,
            detail=e.message,
        )
    except DocumentProcessingError as e:
        logger.error(f"Document processing error: {e.message}")
        raise HTTPException(
            status_code=422,
            detail=e.message,
        )
    except Exception as e:
        logger.error(f"Unexpected error during document upload: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to upload document",
        )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    skip: int = Query(0, ge=0, description="Number of documents to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of documents to return"),
):
    """
    List all uploaded documents with pagination.
    
    Args:
        skip: Number of documents to skip (pagination offset)
        limit: Maximum number of documents to return
        
    Returns:
        DocumentListResponse: List of documents and total count
    """
    try:
        logger.info(f"Listing documents: skip={skip}, limit={limit}")
        
        # Get documents from database
        all_docs = list(documents_db.values())
        total_count = len(all_docs)
        
        # Apply pagination
        paginated_docs = all_docs[skip : skip + limit]
        
        # Convert to response schema
        docs_response = [
            DocumentInfo(
                id=doc["id"],
                name=doc["name"],
                content_type=doc["content_type"],
                size_bytes=doc["size_bytes"],
                chunks_count=doc["chunks_count"],
                uploaded_at=doc["uploaded_at"],
                status=doc["status"],
            )
            for doc in paginated_docs
        ]
        
        return DocumentListResponse(
            documents=docs_response,
            total_count=total_count,
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to list documents",
        )


@router.get("/{doc_id}", response_model=DocumentInfo)
async def get_document(doc_id: str):
    """
    Get information about a specific document.
    
    Args:
        doc_id: The unique document ID
        
    Returns:
        DocumentInfo: Document information
        
    Raises:
        HTTPException: If document is not found
    """
    try:
        logger.info(f"Retrieving document: {doc_id}")
        
        if doc_id not in documents_db:
            logger.warning(f"Document not found: {doc_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {doc_id} not found",
            )
        
        doc = documents_db[doc_id]
        
        return DocumentInfo(
            id=doc["id"],
            name=doc["name"],
            content_type=doc["content_type"],
            size_bytes=doc["size_bytes"],
            chunks_count=doc["chunks_count"],
            uploaded_at=doc["uploaded_at"],
            status=doc["status"],
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve document",
        )


@router.delete("/{doc_id}", status_code=204)
async def delete_document(doc_id: str):
    """
    Delete a document from the system.
    
    Args:
        doc_id: The unique document ID
        
    Raises:
        HTTPException: If document is not found
    """
    try:
        logger.info(f"Deleting document: {doc_id}")
        
        if doc_id not in documents_db:
            logger.warning(f"Document not found for deletion: {doc_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {doc_id} not found",
            )
        
        doc = documents_db[doc_id]
        
        # Delete physical file
        if os.path.exists(doc["file_path"]):
            os.remove(doc["file_path"])
            logger.info(f"Deleted file: {doc['file_path']}")
        
        # Remove from database
        del documents_db[doc_id]
        
        logger.info(f"Document deleted successfully: {doc_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete document",
        )


@router.get("/{doc_id}/content")
async def get_document_content(doc_id: str):
    """
    Get the raw content of a document.
    
    Args:
        doc_id: The unique document ID
        
    Returns:
        dict: Document content
        
    Raises:
        HTTPException: If document is not found
    """
    try:
        logger.info(f"Retrieving document content: {doc_id}")
        
        if doc_id not in documents_db:
            logger.warning(f"Document not found: {doc_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {doc_id} not found",
            )
        
        doc = documents_db[doc_id]
        file_path = doc["file_path"]
        
        # Read file content
        if not os.path.exists(file_path):
            logger.error(f"File not found on disk: {file_path}")
            raise HTTPException(
                status_code=500,
                detail="File not found on disk",
            )
        
        with open(file_path, "rb") as f:
            content = f.read()
        
        return {
            "doc_id": doc_id,
            "name": doc["name"],
            "content_type": doc["content_type"],
            "size_bytes": len(content),
            "content": content.decode("utf-8", errors="ignore"),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document content: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve document content",
        )
