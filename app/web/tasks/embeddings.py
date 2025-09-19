from celery import shared_task
from app.logging import get_module_logger

from app.web.db.models import Pdf
from app.web.files import download
from app.chat import create_embeddings_for_pdf

# Get a logger for embeddings tasks
logger = get_module_logger("celery.tasks.embeddings")


@shared_task()
def process_document(pdf_id: int):
    logger.info(f"Starting to process document with PDF ID: {pdf_id}")

    try:
        pdf = Pdf.find_by(id=pdf_id)
        if not pdf:
            logger.error(f"PDF with ID {pdf_id} not found")
            return

        logger.info(f"Found PDF: {pdf.name}")

        with download(pdf.id) as pdf_path:
            logger.debug(f"Downloaded PDF to: {pdf_path}")
            create_embeddings_for_pdf(pdf.id, pdf_path)
            logger.info(f"Successfully processed embeddings for PDF: {pdf.name}")

    except Exception as e:
        logger.error(f"Failed to process document {pdf_id}: {str(e)}", exc_info=True)
        raise
