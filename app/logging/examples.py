"""
Example usage of the centralized logging service.

This file demonstrates various ways to use the logging service
throughout the application.
"""

from app.logging import get_logger, get_module_logger, configure_logging
from app.logging.config import DevelopmentConfig, ProductionConfig

def basic_usage_example():
    """Basic usage with automatic configuration"""

    # Get a logger for the current module
    logger = get_logger(__name__)

    # Log messages at different levels (will appear in colors!)
    logger.debug("This is a debug message")        # Cyan
    logger.info("Application started successfully") # Green
    logger.warning("This is a warning message")     # Yellow
    logger.error("An error occurred")              # Red
    logger.critical("Critical system error")       # Magenta

def module_specific_example():
    """Example of module-specific loggers"""

    # Get loggers for specific modules
    web_logger = get_module_logger("web.api")
    chat_logger = get_module_logger("chat.embeddings")
    celery_logger = get_module_logger("celery.worker")

    web_logger.info("Processing API request")
    chat_logger.info("Generating embeddings")
    celery_logger.info("Background task started")

def custom_configuration_example():
    """Example of custom logging configuration"""

    # Configure logging for development
    dev_config = DevelopmentConfig()
    configure_logging(dev_config)

    logger = get_logger(__name__)
    logger.debug("Development logging enabled")

    # Later in production, you might do:
    # prod_config = ProductionConfig()
    # configure_logging(prod_config)

def structured_logging_example():
    """Example of structured logging with extra context"""

    logger = get_logger(__name__)

    # Log with extra context
    logger.info("User action performed", extra={
        "user_id": "12345",
        "action": "upload_pdf",
        "file_size": "2.5MB"
    })

    # Log exceptions with context
    try:
        # Some operation that might fail
        result = 10 / 0
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}", exc_info=True)

def web_application_example():
    """Example usage in a Flask web application"""

    logger = get_module_logger("web.views.pdf")

    def upload_pdf():
        logger.info("PDF upload initiated")

        try:
            # PDF processing logic
            logger.debug("Processing PDF file")
            # ... processing ...
            logger.info("PDF processed successfully")

        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}", exc_info=True)
            raise

def chat_module_example():
    """Example usage in the chat module"""

    logger = get_module_logger("chat.vector_stores")

    def initialize_vector_store():
        logger.info("Initializing vector store connection")

        try:
            # Vector store initialization
            logger.debug("Connecting to Pinecone")
            # ... connection logic ...
            logger.info("Vector store initialized successfully")

        except Exception as e:
            logger.warning(f"Vector store initialization failed, using fallback: {str(e)}")
            # Fallback logic
            logger.info("Fallback vector store initialized")

def celery_task_example():
    """Example usage in Celery tasks"""

    logger = get_module_logger("celery.tasks.embeddings")

    def create_embeddings_task(pdf_id):
        logger.info(f"Starting embeddings creation for PDF {pdf_id}")

        try:
            # Task logic
            logger.debug(f"Processing PDF {pdf_id}")
            # ... processing ...
            logger.info(f"Embeddings created successfully for PDF {pdf_id}")

        except Exception as e:
            logger.error(f"Embeddings creation failed for PDF {pdf_id}: {str(e)}", exc_info=True)
            raise

if __name__ == "__main__":
    # Run examples
    print("Running logging examples...")

    basic_usage_example()
    module_specific_example()
    custom_configuration_example()
    structured_logging_example()

    print("Check the logs directory for output files!")