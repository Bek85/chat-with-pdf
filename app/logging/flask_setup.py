"""
Flask application logging setup utilities.
"""

import os
from flask import Flask
from app.logging import configure_logging
from app.logging.config import CONFIGS

def setup_flask_logging(app: Flask) -> None:
    """
    Set up logging for a Flask application based on the environment.

    Args:
        app: Flask application instance
    """
    # Get environment from Flask config or environment variable
    env = app.config.get('ENV') or os.getenv('FLASK_ENV', 'development')

    # Configure logging based on environment
    if env in CONFIGS:
        config_class = CONFIGS[env]
        configure_logging(config_class())
    else:
        # Default configuration
        configure_logging()

    # Disable Flask's default logging if we're handling it
    if not app.debug:
        app.logger.handlers.clear()

def init_app_logging(app: Flask) -> None:
    """
    Initialize logging for the Flask application.
    This should be called during app creation.

    Args:
        app: Flask application instance
    """
    setup_flask_logging(app)

    # Log application startup
    from app.logging import get_module_logger
    logger = get_module_logger("web.app")
    logger.info(f"Flask application starting in {app.config.get('ENV', 'unknown')} mode")