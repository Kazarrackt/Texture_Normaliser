# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.4 - 2025-03-03
# ---

import os
import logging
from datetime import datetime
import re

class Logger:
    """
    Logger class for the Texture Normaliser application.
    """
    def __init__(self, name="TextureNormaliser", log_dir="logs"):
        """
        Initialize the logger.
        
        # Oh look, another logger class. Because the world definitely needed one more of these.
        # At least this one replaces newlines with dashes, so it's basically revolutionary.
        """
        self.name = name
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up logging to file
        self.log_file = os.path.join(log_dir, f"{name.lower()}.log")
        
        # Configure the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', 
                                     datefmt='%Y-%m-%d %H:%M:%S')
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Prevent log messages from being propagated to the root logger
        self.logger.propagate = False
        
    def _format_message(self, message):
        """
        Format the log message by replacing newlines with ' - '.
        
        # Logs with newlines? Not on my watch! We'll replace them with dashes
        # because apparently that's more readable. It's not, but whatever.
        """
        if isinstance(message, str):
            return re.sub(r'\n', ' - ', message)
        return message
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(self._format_message(message))
        
    def info(self, message):
        """Log an info message."""
        self.logger.info(self._format_message(message))
        
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(self._format_message(message))
        
    def error(self, message):
        """Log an error message."""
        self.logger.error(self._format_message(message))
        
    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(self._format_message(message))
        
    def exception(self, message):
        """Log an exception message with traceback."""
        self.logger.exception(self._format_message(message))

# Create a global logger instance
logger = Logger()

if __name__ == "__main__":
    # Test the logger
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    try:
        1/0
    except Exception as e:
        logger.exception(f"This is an exception message: {e}") 