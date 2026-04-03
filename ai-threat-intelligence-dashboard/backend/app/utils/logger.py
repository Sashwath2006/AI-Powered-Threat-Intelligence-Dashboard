"""Logging utility"""
import logging
from app.config import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for a module"""
    return logging.getLogger(name)
