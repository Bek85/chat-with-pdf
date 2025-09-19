from app.web import create_app
from app.logging import configure_logging, get_module_logger
from app.logging.config import ProductionConfig
import os

# Initialize our colorful logging service for Celery
env = os.getenv('FLASK_ENV', 'production')
if env == 'development':
    from app.logging.config import DevelopmentConfig
    configure_logging(DevelopmentConfig())
else:
    configure_logging(ProductionConfig())

# Get a logger for the Celery worker
logger = get_module_logger("celery.worker")

flask_app = create_app()

if "celery" not in flask_app.extensions:
    raise RuntimeError(
        "Celery is not configured. Please set REDIS_URI environment variable."
    )

celery_app = flask_app.extensions["celery"]

logger.info("Celery worker initialized with colorful logging")
