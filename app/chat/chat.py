from app.chat.models import ChatArgs
from langchain.chains import ConversationalRetrievalChain
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)

    return ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, return_source_documents=True
    )
