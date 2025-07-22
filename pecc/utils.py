"""
Common utility functions for PECC system.
Modular and reusable helpers for logging, validation, etc.
"""

import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pecc")

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

# Add more utility functions as needed
