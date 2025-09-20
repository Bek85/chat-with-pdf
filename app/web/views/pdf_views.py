from flask import Blueprint, g, jsonify
from werkzeug.exceptions import Unauthorized
from app.web.hooks import login_required, handle_file_upload, load_model
from app.web.db.models import Pdf
from app.web.db.models.conversation import Conversation
from app.web.db.models.message import Message
from app.web.tasks.embeddings import process_document
from app.web import files

bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")


@bp.route("/", methods=["GET"])
@login_required
def list():
    pdfs = Pdf.where(user_id=g.user.id)

    return Pdf.as_dicts(pdfs)


@bp.route("/", methods=["POST"])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    res, status_code = files.upload(file_path)
    if status_code >= 400:
        return res, status_code

    pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)

    # TODO: Defer this to be processed by the worker
    process_document.delay(pdf.id)

    return pdf.as_dict()


@bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
@load_model(Pdf)
def show(pdf):
    return jsonify(
        {
            "pdf": pdf.as_dict(),
            "download_url": files.create_download_url(pdf.id),
        }
    )


@bp.route("/<string:pdf_id>", methods=["DELETE"])
@login_required
@load_model(Pdf)
def delete(pdf):
    try:
        # Delete the file from storage
        res, status_code = files.delete(pdf.id)
        if status_code >= 400:
            # Log but don't fail the operation if file deletion fails
            pass

        # Delete all conversations and their messages associated with this PDF
        conversations = Conversation.where(pdf_id=pdf.id)
        for conversation in conversations:
            # Delete all messages in this conversation
            messages = Message.where(conversation_id=conversation.id)
            for message in messages:
                message.delete(commit=False)

            # Delete the conversation
            conversation.delete(commit=False)

        # Delete the PDF record from database
        pdf.delete(commit=False)

        # Commit all deletions together
        from app.web.db import db
        db.session.commit()

        return {"message": "PDF deleted successfully"}, 200
    except Exception as e:
        from app.web.db import db
        db.session.rollback()
        return {"error": f"Failed to delete PDF: {str(e)}"}, 500
