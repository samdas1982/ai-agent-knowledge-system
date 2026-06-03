"""
Health and status check endpoints.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.config import get_settings
from app.utils.logger import setup_logger
from app.api.schemas import HealthResponse, StatusResponse

logger = setup_logger(__name__)
settings = get_settings()

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint (Status Code: 200).
    
    Verifies that the application is running and responsive.
    
    Returns:
        HealthResponse: Health status information
    """
    logger.debug("Health check requested")
    
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        environment=settings.app_env,
        version=settings.api_version,
        timestamp=datetime.utcnow(),
    )


@router.get("/api/status", response_model=StatusResponse)
async def system_status():
    """
    Get comprehensive system status.
    
    Returns:
        StatusResponse: Detailed system status
    """
    try:
        logger.info("System status requested")
        
        # TODO: Implement actual checks for:
        # - Vector DB connection
        # - LLM availability
        # - Document count
        # - Chunk count
        # - Embeddings cache
        
        return StatusResponse(
            status="operational",
            vector_db_connected=True,
            llm_available=True,
            documents_count=0,
            total_chunks=0,
            embeddings_cached=0,
        )
        
    except Exception as e:
        logger.error(f"Error checking system status: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to check system status",
        )
