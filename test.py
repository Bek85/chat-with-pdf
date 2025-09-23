from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat = init_chat_model(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])


messages = prompt.format_messages(content="tell me a joke")

output = chat.invoke(messages)

print(output)
