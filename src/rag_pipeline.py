"""
RAG Pipeline for TrustVoice Analytics
Handles data processing, vectorization, and retrieval for financial complaints analysis
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json

from config import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
    DEFAULT_TOP_K,
    SIMILARITY_THRESHOLD,
    RAW_DATA_PATH,
    FILTERED_DATA_PATH
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline for financial complaints analysis
    """
    
    def __init__(self, use_existing_vector_store: bool = True):
        """
        Initialize the RAG pipeline
        
        Args:
            use_existing_vector_store: Whether to use existing ChromaDB or create new one
        """
        self.use_existing_vector_store = use_existing_vector_store
        self.chroma_client = None
        self.collection = None
        self.embedding_model = None
        self.complaints_data = None
        
        # Initialize components
        self._initialize_chroma_client()
        self._initialize_embedding_model()
        
    def _initialize_chroma_client(self):
        """Initialize ChromaDB client"""
        try:
            # Create persistent ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=str(CHROMA_DB_PATH),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info(f"✅ ChromaDB client initialized at {CHROMA_DB_PATH}")
            
            # Get or create collection
            try:
                self.collection = self.chroma_client.get_collection(CHROMA_COLLECTION_NAME)
                logger.info(f"✅ Using existing collection: {CHROMA_COLLECTION_NAME}")
            except:
                if not self.use_existing_vector_store:
                    self.collection = self.chroma_client.create_collection(
                        name=CHROMA_COLLECTION_NAME,
                        metadata={"description": "Financial complaints embeddings"}
                    )
                    logger.info(f"✅ Created new collection: {CHROMA_COLLECTION_NAME}")
                else:
                    logger.warning(f"⚠️ Collection {CHROMA_COLLECTION_NAME} not found")
                    self.collection = None
                    
        except Exception as e:
            logger.error(f"❌ Error initializing ChromaDB: {e}")
            self.chroma_client = None
            self.collection = None
    
    def _initialize_embedding_model(self):
        """Initialize the sentence transformer model"""
        try:
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            logger.info(f"✅ Embedding model loaded: {EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"❌ Error loading embedding model: {e}")
            self.embedding_model = None
    
    def load_data(self, data_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load complaints data from CSV file
        
        Args:
            data_path: Path to the CSV file (optional)
            
        Returns:
            DataFrame containing the complaints data
        """
        try:
            if data_path is None:
                # Try to find data files
                data_files = list(RAW_DATA_PATH.glob("*.csv"))
                if not data_files:
                    logger.warning("No CSV files found in data/raw/")
                    return pd.DataFrame()
                data_path = str(data_files[0])
            
            logger.info(f"Loading data from {data_path}")
            self.complaints_data = pd.read_csv(data_path)
            logger.info(f"✅ Loaded {len(self.complaints_data)} complaints")
            return self.complaints_data
            
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return pd.DataFrame()
    
    def preprocess_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the complaints data
        
        Returns:
            Preprocessed DataFrame
        """
        if self.complaints_data is None or self.complaints_data.empty:
            logger.error("No data loaded. Call load_data() first.")
            return pd.DataFrame()
        
        logger.info("🔄 Preprocessing complaints data...")
        
        # Make a copy to avoid modifying original
        df = self.complaints_data.copy()
        
        # Basic preprocessing steps
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate rows")
        
        # Handle missing values
        df = df.fillna("")
        
        # Convert text columns to string
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].astype(str)
        
        # Create a combined text field for embedding
        if 'consumer_complaint_narrative' in df.columns:
            df['combined_text'] = df['consumer_complaint_narrative']
        else:
            # Combine multiple text fields if available
            text_fields = ['company', 'product', 'issue']
            available_fields = [f for f in text_fields if f in df.columns]
            if available_fields:
                df['combined_text'] = df[available_fields].apply(
                    lambda x: ' '.join(x.astype(str)), axis=1
                )
            else:
                df['combined_text'] = df.iloc[:, 0].astype(str)  # Use first column
        
        self.complaints_data = df
        logger.info(f"✅ Preprocessed {len(df)} complaints")
        return df
    
    def create_embeddings(self, text_column: str = "combined_text") -> np.ndarray:
        """
        Create embeddings for the complaints text
        
        Args:
            text_column: Column containing the text to embed
            
        Returns:
            Array of embeddings
        """
        if self.embedding_model is None:
            logger.error("Embedding model not initialized")
            return np.array([])
        
        if self.complaints_data is None or self.complaints_data.empty:
            logger.error("No data loaded. Call load_data() first.")
            return np.array([])
        
        if text_column not in self.complaints_data.columns:
            logger.error(f"Column {text_column} not found in data")
            return np.array([])
        
        logger.info("🔄 Creating embeddings...")
        
        try:
            texts = self.complaints_data[text_column].tolist()
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            
            logger.info(f"✅ Created embeddings for {len(embeddings)} complaints")
            return embeddings
            
        except Exception as e:
            logger.error(f"❌ Error creating embeddings: {e}")
            return np.array([])
    
    def build_vector_store(self, embeddings: np.ndarray) -> bool:
        """
        Build ChromaDB vector store with embeddings
        
        Args:
            embeddings: Array of embeddings
            
        Returns:
            True if successful, False otherwise
        """
        if self.collection is None:
            logger.error("ChromaDB collection not initialized")
            return False
        
        if len(embeddings) == 0:
            logger.error("No embeddings provided")
            return False
        
        logger.info("🔄 Building vector store...")
        
        try:
            # Prepare data for ChromaDB
            texts = self.complaints_data['combined_text'].tolist()
            metadatas = self.complaints_data.to_dict('records')
            ids = [f"complaint_{i}" for i in range(len(texts))]
            
            # Add embeddings to ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✅ Vector store built with {len(ids)} documents")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error building vector store: {e}")
            return False
    
    def search_similar_complaints(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Search for similar complaints based on a query
        
        Args:
            query: Search query
            top_k: Number of similar complaints to return
            
        Returns:
            List of similar complaints with metadata
        """
        if self.collection is None:
            logger.error("ChromaDB collection not initialized")
            return []
        
        if top_k is None:
            top_k = DEFAULT_TOP_K
        
        logger.info(f"🔍 Searching for complaints similar to: {query}")
        
        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=top_k,
                include=['metadatas', 'documents', 'distances']
            )
            
            # Format results
            similar_complaints = []
            if results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    complaint_info = metadata.copy()
                    complaint_info['similarity_score'] = 1 - results['distances'][0][i]  # Convert distance to similarity
                    complaint_info['document'] = results['documents'][0][i] if results['documents'] and results['documents'][0] else ""
                    similar_complaints.append(complaint_info)
            
            logger.info(f"✅ Found {len(similar_complaints)} similar complaints")
            return similar_complaints
            
        except Exception as e:
            logger.error(f"❌ Error searching complaints: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the ChromaDB collection"""
        if self.collection is None:
            return {"error": "Collection not initialized"}
        
        try:
            count = self.collection.count()
            return {
                "collection_name": CHROMA_COLLECTION_NAME,
                "document_count": count,
                "embedding_dimension": EMBEDDING_DIMENSION,
                "embedding_model": EMBEDDING_MODEL
            }
        except Exception as e:
            return {"error": f"Error getting collection info: {e}"}
    
    def run_pipeline(self, data_path: Optional[str] = None) -> bool:
        """
        Run the complete RAG pipeline
        
        Args:
            data_path: Path to the data file (optional)
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("🚀 Starting RAG pipeline...")
        
        try:
            # Load data
            self.load_data(data_path)
            
            # Preprocess data
            self.preprocess_data()
            
            # Only build vector store if not using existing one
            if not self.use_existing_vector_store:
                # Create embeddings
                embeddings = self.create_embeddings()
                
                # Build vector store
                if not self.build_vector_store(embeddings):
                    return False
            
            logger.info("✅ RAG pipeline completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ RAG pipeline failed: {e}")
            return False

def main():
    """Example usage of the RAG pipeline"""
    # Initialize pipeline
    pipeline = RAGPipeline(use_existing_vector_store=True)
    
    # Run pipeline
    success = pipeline.run_pipeline()
    
    if success:
        # Get collection info
        info = pipeline.get_collection_info()
        print(f"Collection info: {info}")
        
        # Example search
        results = pipeline.search_similar_complaints("credit card fraud", top_k=3)
        print(f"Found {len(results)} similar complaints")
        
        for i, result in enumerate(results, 1):
            print(f"\nComplaint {i}:")
            print(f"Company: {result.get('company', 'N/A')}")
            print(f"Product: {result.get('product', 'N/A')}")
            print(f"Similarity: {result.get('similarity_score', 0):.3f}")
    else:
        print("❌ RAG pipeline failed")

if __name__ == "__main__":
    main() 