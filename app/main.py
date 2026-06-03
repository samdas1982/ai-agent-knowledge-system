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
from app.api.routes import documents, queries, health

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
    logger.info(f"API listening on {settings.api_host}:{settings.api_port}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    description="AI-powered agent system for querying enterprise documents using RAG and Agentic AI",
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


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information and useful links
    """
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "description": "AI Agent Knowledge System - Enterprise Document Query Platform",
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "health_check": "/health",
        "status": "/api/status",
        "endpoints": {
            "documents": "/api/documents",
            "queries": "/api/queries",
        },
    }


# Include routers
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(queries.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower(),
    )
