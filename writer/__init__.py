"""
Writer Package

This package contains the core functionality for the AI Content Writer application.
It includes modules for AI content generation, search engine integration, and utility functions.
"""
import logging

from writer.utils.logging_config import setup_logging, is_running_in_docker

# Initialize logging when the package is imported
# This ensures logging is set up before any other modules are imported
# In Docker, we use a higher log level for console output to reduce noise
if is_running_in_docker():
    # Use INFO level in Docker to ensure important logs are visible
    setup_logging(log_level=logging.INFO, log_to_file=False, log_to_console=True)
else:
    # In development, use more detailed logging with file output
    setup_logging(log_level=logging.DEBUG, log_to_file=True, log_to_console=True)
