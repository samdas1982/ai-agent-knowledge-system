"""
Logging configuration for the application.
Uses loguru for enhanced logging capabilities.
"""

import logging
import sys
from loguru import logger as loguru_logger
from app.config import get_settings

settings = get_settings()


def setup_logger(name: str = __name__):
    """
    Configure loguru logger with appropriate format and level.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    # Remove default handler
    loguru_logger.remove()

    # Add console handler
    loguru_logger.add(
        sys.stdout,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # Add file handler (if log_dir is configured)
    if settings.log_dir:
        loguru_logger.add(
            f"{settings.log_dir}/app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=settings.log_level,
            rotation="500 MB",
            retention="10 days",
        )

    return loguru_logger


# Create a bridge between loguru and standard logging
class InterceptHandler(logging.Handler):
    """Intercept standard logging calls and redirect to loguru."""

    def emit(self, record: logging.LogRecord):
        """Emit log record through loguru."""
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        loguru_logger.log(level, record.getMessage())


# Redirect standard logging to loguru
logging.basicConfig(handlers=[InterceptHandler()], level=settings.log_level)
