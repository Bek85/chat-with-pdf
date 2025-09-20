from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import os
from app.chat.embeddings.openai import embeddings
from app.logging import get_module_logger
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Set up logging
logger = get_module_logger("chat.vector_stores.pinecone")

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


def delete_embeddings_for_pdf(pdf_id: str):
    """Delete all embeddings associated with a specific PDF ID"""
    try:
        if not PINECONE_API_KEY:
            logger.warning("PINECONE_API_KEY not set, skipping Pinecone cleanup")
            return False

        logger.info(f"Starting Pinecone cleanup for PDF ID: {pdf_id}")
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Check if index exists
        indexes = pc.list_indexes()
        index_names = [index_info["name"] for index_info in indexes]
        logger.info(f"Available indexes: {index_names}")

        if PINECONE_INDEX_NAME not in index_names:
            logger.warning(f"Pinecone index '{PINECONE_INDEX_NAME}' does not exist, skipping cleanup")
            return False

        index = pc.Index(PINECONE_INDEX_NAME)

        # Check index stats before deletion
        stats_before = index.describe_index_stats()
        logger.info(f"Index stats before deletion: {stats_before}")

        # Try multiple deletion approaches since metadata filtering can be tricky

        # Approach 1: Direct metadata filter (what we tried before)
        try:
            delete_response = index.delete(
                filter={"pdf_id": pdf_id}
            )
            logger.info(f"Delete response with simple filter: {delete_response}")
        except Exception as e:
            logger.warning(f"Simple filter deletion failed: {e}")

        # Approach 2: Try with explicit equality operator
        try:
            delete_response = index.delete(
                filter={"pdf_id": {"$eq": pdf_id}}
            )
            logger.info(f"Delete response with $eq filter: {delete_response}")
        except Exception as e:
            logger.warning(f"$eq filter deletion failed: {e}")

        # Approach 3: Delete all vectors and recreate (if needed)
        # This is more aggressive but ensures cleanup
        try:
            # First query to get vector IDs with this pdf_id
            query_response = index.query(
                vector=[0.01] * 1536,  # Small non-zero vector
                filter={"pdf_id": pdf_id},
                top_k=10000,  # Large number to get all matches
                include_metadata=True
            )

            if query_response.matches:
                vector_ids = [match.id for match in query_response.matches]
                logger.info(f"Found {len(vector_ids)} vectors to delete for pdf_id={pdf_id}")

                # Log sample metadata for debugging
                for i, match in enumerate(query_response.matches[:3]):
                    logger.info(f"Sample vector {i}: ID={match.id}, metadata={match.metadata}")

                # Delete by IDs
                if vector_ids:
                    delete_response = index.delete(ids=vector_ids)
                    logger.info(f"Delete by IDs response: {delete_response}")
            else:
                logger.warning(f"No vectors found with pdf_id={pdf_id} during query")

        except Exception as e:
            logger.error(f"Query and delete by IDs failed: {e}")

        # Check stats after deletion
        stats_after = index.describe_index_stats()
        logger.info(f"Index stats after deletion: {stats_after}")

        logger.info(f"Completed Pinecone cleanup attempt for PDF {pdf_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting embeddings for PDF {pdf_id} from Pinecone: {str(e)}", exc_info=True)
        return False


# Initialize the vector store
vector_store = initialize_pinecone()
