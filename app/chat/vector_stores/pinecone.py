from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import os
from app.chat.embeddings.openai import embeddings
import logging
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Pinecone credentials from environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENV_NAME", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "docs")


def create_fallback_vector_store():
    """Create a simple in-memory vector store as fallback"""
    from langchain.vectorstores import FAISS
    from langchain.schema import Document

    # Create a dummy document for initialization
    docs = [Document(page_content="Fallback store initialized", metadata={})]
    return FAISS.from_documents(docs, embeddings)


def initialize_pinecone():
    """Initialize Pinecone client and return the vector store"""
    try:
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY environment variable not set")

        logger.info(f"Initializing Pinecone with environment: {PINECONE_ENVIRONMENT}")
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # List existing indexes
        indexes = pc.list_indexes()
        index_names = [index_info["name"] for index_info in indexes]
        logger.info(f"Available Pinecone indexes: {index_names}")

        # Check if index exists
        if PINECONE_INDEX_NAME not in index_names:
            logger.error(f"Pinecone index '{PINECONE_INDEX_NAME}' does not exist")
            return create_fallback_vector_store()

        # Get the index
        index = pc.Index(PINECONE_INDEX_NAME)

        # Initialize the vector store
        vector_store = PineconeVectorStore(index=index, embedding=embeddings)

        logger.info("Successfully connected to Pinecone index")
        return vector_store

    except Exception as e:
        logger.error(f"Error initializing Pinecone: {str(e)}")
        return create_fallback_vector_store()


# Initialize the vector store
vector_store = initialize_pinecone()
