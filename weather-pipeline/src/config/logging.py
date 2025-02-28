import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the default logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log message format
)

logger = logging.getLogger(__name__)  # Create a logger for this module

# Example of logging usage
logger.info("Logging is set up.")  # Log an informational message