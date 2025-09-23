from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")


@bp.route("/", methods=["GET"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]


@bp.route("/", methods=["POST"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    input = request.json.get("input")
    streaming = request.args.get("stream", False)

    pdf = conversation.pdf

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
            "pdf_id": pdf.id,
        },
    )

    from app.chat.memories.sql_memory import SqlMessageHistory
    from app.web.api import get_messages_by_conversation_id

    chat = build_chat(chat_args)
    sql_memory = SqlMessageHistory(conversation_id=conversation.id)

    if not chat:
        return "Chat not yet implemented!"

    # Get chat history for the chain - directly from the API
    chat_history = get_messages_by_conversation_id(conversation.id)

    if streaming:
        return Response(
            stream_with_context(chat.stream({"question": input, "chat_history": chat_history})), mimetype="text/event-stream"
        )
    else:
        # Simple approach: just run the chain
        from langchain.schema import HumanMessage, AIMessage

        # Add user message to memory
        sql_memory.add_message(HumanMessage(content=input))

        # Run chain with the question and chat history
        result = chat.invoke({"question": input, "chat_history": chat_history})
        answer = result["answer"]

        # Add AI response to memory
        sql_memory.add_message(AIMessage(content=answer))

        return jsonify({"role": "assistant", "content": answer})
