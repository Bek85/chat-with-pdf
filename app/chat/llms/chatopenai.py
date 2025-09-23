from langchain.chat_models import init_chat_model


def build_llm(chat_args):
    return init_chat_model(model="gpt-4o-mini")
