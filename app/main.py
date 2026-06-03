"""
FastAPI application entry point for the AI Agent Knowledge System.
Initializes routes, middleware, and application configuration.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.utils.logger import setup_logger

# Configure logging
logger = setup_logger(__name__)
settings = get_settings()


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.app_name} in {settings.app_env} environment")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Vector DB: {settings.vector_db_type}")
    logger.info(f"LLM Model: {settings.llm_model}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    description="AI-powered agent system for querying enterprise documents using RAG",
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__,
        },
    )


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
        "version": settings.api_version,
    }


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information
    """
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "description": "AI Agent Knowledge System - Enterprise Document Query Platform",
        "documentation": "/docs",
        "health_check": "/health",
    }


# Import and include routers (to be created in Task 2)
# from app.api.routes import documents, queries, health


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower(),
    )
