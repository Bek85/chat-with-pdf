from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import time
from langchain_core.callbacks.base import BaseCallbackHandler

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(f"Callback: {token}")  # Added prefix to distinguish


chat = init_chat_model(model="gpt-4o-mini", streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])

messages = prompt.format_messages(content="tell me a joke")

chain = prompt | chat

# Option A: Just use the callback (simpler)
# Then just invoke (no manual streaming loop needed)
# response = chat.invoke(messages, config={"callbacks": [StreamingHandler()]})

# Option B: Just use manual streaming (no callback)
for chunk in chain.stream(messages):
    print(chunk.content, end="", flush=True)
    time.sleep(0.05)
