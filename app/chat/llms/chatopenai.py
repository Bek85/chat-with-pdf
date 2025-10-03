from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult, ChatGenerationChunk
from typing import List, Optional, Any, Iterator
from langchain_core.callbacks import CallbackManagerForLLMRun
import os


class FallbackChatModel(BaseChatModel):
    """Chat model with automatic fallback from OpenAI to DeepSeek on quota errors."""

    primary: Optional[ChatOpenAI] = None
    fallback: Optional[ChatOpenAI] = None
    use_fallback: bool = False
    streaming: bool = False

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, streaming=False, **kwargs):
        super().__init__(streaming=streaming, **kwargs)
        self.primary = ChatOpenAI(
            model="gpt-4o-mini",
            streaming=streaming,
            max_retries=0  # Disable retries so fallback triggers immediately
        )
        self.streaming = streaming

    def _get_fallback(self):
        if self.fallback is None:
            self.fallback = ChatOpenAI(
                model="deepseek-chat",
                openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
                openai_api_base=os.getenv("DEEPSEEK_BASE_URL"),
                streaming=self.streaming,
            )
        return self.fallback

    def _handle_error(self, e, method, *args, **kwargs):
        if "rate_limit" in str(e).lower() or "quota" in str(e).lower() or "429" in str(e):
            print("OpenAI quota exceeded, switching to DeepSeek...")
            self.use_fallback = True
            return getattr(self._get_fallback(), method)(*args, **kwargs)
        raise

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs) -> ChatResult:
        if self.use_fallback:
            return self._get_fallback()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
        try:
            return self.primary._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
        except Exception as e:
            if "rate_limit" in str(e).lower() or "quota" in str(e).lower() or "429" in str(e):
                print("OpenAI quota exceeded, switching to DeepSeek...")
                self.use_fallback = True
                return self._get_fallback()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
            else:
                raise

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        if self.use_fallback:
            yield from self._get_fallback()._stream(messages, stop=stop, run_manager=run_manager, **kwargs)
            return

        try:
            # Create an iterator from the primary stream
            stream_iter = self.primary._stream(messages, stop=stop, run_manager=run_manager, **kwargs)
            # Try to get the first chunk to trigger any connection errors
            first_chunk = next(stream_iter)
            # If successful, yield the first chunk and continue
            yield first_chunk
            yield from stream_iter
        except Exception as e:
            if "rate_limit" in str(e).lower() or "quota" in str(e).lower() or "429" in str(e):
                print("OpenAI quota exceeded, switching to DeepSeek...")
                self.use_fallback = True
                yield from self._get_fallback()._stream(messages, stop=stop, run_manager=run_manager, **kwargs)
            else:
                raise

    @property
    def _llm_type(self) -> str:
        return "fallback_chat_openai"

    def __getattr__(self, name):
        """Delegate all other attributes to the active model."""
        if name in ['primary', 'fallback', 'use_fallback', 'streaming']:
            return super().__getattribute__(name)
        if self.use_fallback:
            return getattr(self._get_fallback(), name)
        return getattr(self.primary, name)


def build_llm(chat_args):
    return FallbackChatModel(streaming=chat_args.streaming)
