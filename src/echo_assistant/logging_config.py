"""Logging configuration for E.C.H.O Assistant."""

import logging
import sys
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """Configure unified logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / 'echo_assistant.log')
        ]
    )
    
    return logging.getLogger('echo_assistant')
