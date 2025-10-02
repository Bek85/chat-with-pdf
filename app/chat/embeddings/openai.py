import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use HuggingFace embeddings (dimension 384) for the new Pinecone index
print("Using HuggingFace embeddings (dimension 384)")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
