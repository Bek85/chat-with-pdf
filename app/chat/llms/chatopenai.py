from langchain.chat_models import init_chat_model
import os


def build_llm(chat_args):
    try:
        return init_chat_model(model="gpt-4o-mini")
    except Exception as e:
        if "rate_limit" in str(e).lower() or "quota" in str(e).lower() or "429" in str(e):
            # Fallback to DeepSeek when OpenAI quota is exceeded
            return init_chat_model(
                model="deepseek-chat",
                model_provider="openai",
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("DEEPSEEK_BASE_URL")
            )
        raise
