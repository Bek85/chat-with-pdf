#!/usr/bin/env python3
"""
Script to create a new Pinecone index with HuggingFace embeddings dimensions
"""
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Configuration for new index
INDEX_NAME = "docs-hf"  # New index name
DIMENSION = 384  # HuggingFace all-MiniLM-L6-v2 dimension
METRIC = "cosine"

# Create index
print(f"Creating Pinecone index '{INDEX_NAME}' with dimension {DIMENSION}...")

try:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(
            cloud="aws",
            region=os.getenv("PINECONE_ENV_NAME", "us-east-1")
        )
    )
    print(f"✅ Successfully created index '{INDEX_NAME}'")
    print(f"\nNext steps:")
    print(f"1. Update your .env file:")
    print(f"   PINECONE_INDEX_NAME={INDEX_NAME}")
    print(f"2. Get the index host:")

    # Wait for index to be ready and get host
    index = pc.Index(INDEX_NAME)
    print(f"   PINECONE_HOST={index.describe_index_stats()}")

except Exception as e:
    print(f"❌ Error creating index: {e}")
    print("\nIf index already exists, you can either:")
    print("1. Use a different index name")
    print("2. Delete the existing index first")
