from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import time

load_dotenv()

chat = init_chat_model(model="gpt-4o-mini", streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])

messages = prompt.format_messages(
    content="tell me a short story about a magical forest"
)

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
    time.sleep(0.05)  # Add 50ms delay between chunks
