"""
Configuration file for TrustVoice Analytics RAG Pipeline
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
GOOGLE_DRIVE_DIR = BASE_DIR / "google_drive"

# Google Drive configuration
GOOGLE_DRIVE_FOLDER_ID = "1HBvnKK6oTGSu3XLZrofQCWdD18Siens0?usp=sharing"
GOOGLE_DRIVE_CREDENTIALS_FILE = GOOGLE_DRIVE_DIR / "credentials.json"
GOOGLE_DRIVE_TOKEN_FILE = GOOGLE_DRIVE_DIR / "token.json"

# Vector store configuration
CHROMA_DB_PATH = VECTOR_STORE_DIR / "chromadb_sample_dataset"
CHROMA_COLLECTION_NAME = "financial_complaints"

# Data paths
RAW_DATA_PATH = DATA_DIR / "raw"
FILTERED_DATA_PATH = DATA_DIR / "filtered"

# Model configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
SIMILARITY_METRIC = "cosine"

# Search configuration
DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.7

# Application configuration
STREAMLIT_PORT = 8501
STREAMLIT_HOST = "0.0.0.0"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs" / "trustvoice.log"

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        DATA_DIR,
        RAW_DATA_PATH,
        FILTERED_DATA_PATH,
        VECTOR_STORE_DIR,
        GOOGLE_DRIVE_DIR,
        LOG_FILE.parent
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

# Environment variables
def get_google_drive_credentials():
    """Get Google Drive credentials from environment variables"""
    return {
        "client_id": os.getenv("GOOGLE_DRIVE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_DRIVE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_DRIVE_REDIRECT_URI", "http://localhost:8080")
    }

# Initialize directories on import
create_directories() 