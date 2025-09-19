from celery import shared_task

from app.web.db.models import Pdf
from app.web.files import download
from app.chat import create_embeddings_for_pdf


@shared_task()
def process_document(pdf_id: int):
    print(f"Starting to process document with PDF ID: {pdf_id}")
    pdf = Pdf.find_by(id=pdf_id)
    print(f"Found PDF: {pdf.name if pdf else 'None'}")
    with download(pdf.id) as pdf_path:
        print(f"Downloaded PDF to: {pdf_path}")
        create_embeddings_for_pdf(pdf.id, pdf_path)
