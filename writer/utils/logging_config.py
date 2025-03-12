"""
Logging Configuration Module

This module provides a centralized configuration for logging throughout the application.
It sets up logging handlers, formatters, and log levels for consistent logging.
"""
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Default log directory
LOG_DIR = "logs"

# Check if running in Docker
def is_running_in_docker():
    """Check if the application is running inside a Docker container."""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

def setup_logging(log_level=logging.INFO, log_to_file=True, log_to_console=True):
    """
    Set up logging configuration for the application.
    
    This function configures the root logger with the specified log level and handlers.
    It creates a consistent logging format across the application and optionally
    sets up file logging with rotation.
    
    Args:
        log_level (int): The logging level to use (default: logging.INFO)
        log_to_file (bool): Whether to log to a file (default: True)
        log_to_console (bool): Whether to log to the console (default: True)
        
    Returns:
        logging.Logger: The configured root logger
    """
    # Create the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter - simpler format for Docker to make logs more readable
    if is_running_in_docker():
        formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Add console handler if requested
    if log_to_console:
        # In Docker, we want to ensure logs go to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Add file handler if requested and not in Docker
    # In Docker, we'll rely on console logging which gets captured by the container logs
    if log_to_file and not is_running_in_docker():
        # Create log directory if it doesn't exist
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        
        # Create a timestamped log file name
        log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
        
        # Set up rotating file handler (10MB max size, keep 5 backup files)
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger

def get_logger(name):
    """
    Get a logger with the specified name.
    
    This is a convenience function to get a logger with the specified name.
    It ensures that all loggers use the same naming convention and inherit
    from the root logger configuration.
    
    Args:
        name (str): The name of the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: A logger instance with the specified name
    """
    return logging.getLogger(name)
