"""
Document ingestion service that orchestrates the full pipeline.
Combines document processing, chunking, validation, and storage.
"""

import uuid
from datetime import datetime
from typing import Dict, List
import logging

from app.config import get_settings
from app.utils.logger import setup_logger
from app.utils.errors import DocumentProcessingError
from app.core.document_processor import DocumentProcessor
from app.core.chunking_service import ChunkingService
from app.core.data_validator import DataValidator

logger = setup_logger(__name__)
settings = get_settings()


class DocumentIngestionService:
    """Orchestrates the document ingestion pipeline."""

    def __init__(self):
        """Initialize ingestion service."""
        self.document_processor = DocumentProcessor()
        self.chunking_service = ChunkingService()
        self.data_validator = DataValidator()
        logger.info("DocumentIngestionService initialized")

    def ingest_document(self, file_path: str) -> Dict:
        """
        Complete document ingestion pipeline.
        
        Steps:
        1. Process document and extract text
        2. Validate extracted data
        3. Clean and normalize text
        4. Extract metadata and entities
        5. Chunk document into segments
        6. Validate chunks
        
        Args:
            file_path: Path to document file
            
        Returns:
            dict: Ingestion result with processed chunks
            
        Raises:
            DocumentProcessingError: If ingestion fails
        """
        try:
            logger.info(f"Starting document ingestion: {file_path}")
            
            # Step 1: Extract text from document
            logger.debug("Step 1: Processing document...")
            doc_result = self.document_processor.process_document(file_path)
            content = doc_result["content"]
            
            # Step 2: Validate extracted text
            logger.debug("Step 2: Validating text...")
            if not self.data_validator.validate_text(content):
                raise DocumentProcessingError("Extracted text failed validation")
            
            # Step 3: Extract metadata
            logger.debug("Step 3: Extracting metadata...")
            metadata = self.document_processor.extract_metadata(file_path)
            metadata["ingestion_date"] = datetime.utcnow().isoformat()
            metadata["document_id"] = str(uuid.uuid4())
            metadata["detected_language"] = self.data_validator.detect_language(content)
            
            # Step 4: Detect entities
            logger.debug("Step 4: Extracting entities...")
            entities = self.data_validator.extract_entities(content)
            
            # Step 5: Remove boilerplate
            logger.debug("Step 5: Removing boilerplate...")
            cleaned_content = self.data_validator.remove_boilerplate(content)
            
            # Step 6: Chunk document
            logger.debug("Step 6: Chunking document...")
            chunks = self.chunking_service.chunk_document(cleaned_content, metadata)
            
            # Step 7: Validate chunks
            logger.debug("Step 7: Validating chunks...")
            is_valid, validation_msg = self.chunking_service.validate_chunks(chunks)
            
            if not is_valid:
                logger.warning(f"Chunk validation warning: {validation_msg}")
            
            ingestion_result = {
                "success": True,
                "document_id": metadata["document_id"],
                "file_path": file_path,
                "metadata": metadata,
                "entities": entities,
                "chunks": chunks,
                "chunk_count": len(chunks),
                "total_tokens": sum(c.get("word_count", 0) for c in chunks),
                "validation": {
                    "is_valid": is_valid,
                    "message": validation_msg,
                },
                "status": "ingested",
            }
            
            logger.info(
                f"Document ingestion completed successfully. "
                f"ID: {metadata['document_id']}, Chunks: {len(chunks)}"
            )
            
            return ingestion_result
            
        except DocumentProcessingError:
            raise
        except Exception as e:
            logger.error(f"Document ingestion failed: {str(e)}", exc_info=e)
            raise DocumentProcessingError(f"Document ingestion failed: {str(e)}")

    def batch_ingest(self, file_paths: List[str]) -> Dict:
        """
        Ingest multiple documents.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            dict: Batch ingestion results
        """
        logger.info(f"Starting batch ingestion of {len(file_paths)} documents")
        
        results = {
            "total_documents": len(file_paths),
            "successful": 0,
            "failed": 0,
            "documents": [],
            "errors": [],
        }
        
        for file_path in file_paths:
            try:
                result = self.ingest_document(file_path)
                results["successful"] += 1
                results["documents"].append(result)
            except Exception as e:
                logger.error(f"Failed to ingest {file_path}: {str(e)}")
                results["failed"] += 1
                results["errors"].append({
                    "file_path": file_path,
                    "error": str(e),
                })
        
        logger.info(
            f"Batch ingestion completed. "
            f"Successful: {results['successful']}, Failed: {results['failed']}"
        )
        
        return results

    def estimate_chunks(self, text: str) -> Dict:
        """
        Estimate number of chunks without actually chunking.
        
        Args:
            text: Text to estimate
            
        Returns:
            dict: Estimation results
        """
        try:
            text_length = len(text)
            word_count = len(text.split())
            
            # Rough estimation based on chunk size
            estimated_chunks = max(1, text_length // settings.chunk_size)
            
            return {
                "text_length": text_length,
                "word_count": word_count,
                "chunk_size": settings.chunk_size,
                "estimated_chunks": estimated_chunks,
            }
            
        except Exception as e:
            logger.error(f"Error estimating chunks: {str(e)}")
            return {"error": str(e)}
