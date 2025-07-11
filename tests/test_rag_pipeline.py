"""
Unit tests for the RAG pipeline
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_pipeline import RAGPipeline


class TestRAGPipeline:
    """Test cases for RAGPipeline class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.pipeline = RAGPipeline()
        
    def test_pipeline_initialization(self):
        """Test RAGPipeline initialization"""
        assert self.pipeline.data_path == "data/raw/cfpb_complaints.csv"
        assert self.pipeline.complaints_data is None
        assert self.pipeline.vector_store is None

    def test_pipeline_initialization_with_custom_path(self):
        """Test RAGPipeline initialization with custom data path"""
        custom_path = "custom/path/data.csv"
        pipeline = RAGPipeline(data_path=custom_path)
        assert pipeline.data_path == custom_path

    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        """Test successful data loading"""
        # Mock data
        mock_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B'],
            'product': ['Credit Card', 'Mortgage'],
            'consumer_complaint_narrative': ['Complaint 1', 'Complaint 2']
        })
        mock_read_csv.return_value = mock_data
        
        result = self.pipeline.load_data()
        
        assert result.equals(mock_data)
        assert self.pipeline.complaints_data.equals(mock_data)
        mock_read_csv.assert_called_once_with(self.pipeline.data_path)

    @patch('pandas.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        """Test data loading when file is not found"""
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        result = self.pipeline.load_data()
        
        assert result.empty
        assert self.pipeline.complaints_data is None

    def test_preprocess_data_no_data_loaded(self):
        """Test preprocessing when no data is loaded"""
        result = self.pipeline.preprocess_data()
        assert result.empty

    def test_preprocess_data_with_data(self):
        """Test data preprocessing"""
        # Create test data
        test_data = pd.DataFrame({
            'company': ['Bank A', 'Bank A', 'Bank B'],
            'product': ['Credit Card', 'Credit Card', 'Mortgage'],
            'consumer_complaint_narrative': ['Complaint 1', 'Complaint 1', 'Complaint 2']
        })
        self.pipeline.complaints_data = test_data.copy()
        
        result = self.pipeline.preprocess_data()
        
        # Check that duplicates are removed
        assert len(result) == 2  # Should remove one duplicate
        assert len(self.pipeline.complaints_data) == 2

    def test_create_embeddings_valid_column(self):
        """Test embedding creation with valid column"""
        # Create test data
        test_data = pd.DataFrame({
            'consumer_complaint_narrative': ['Complaint 1', 'Complaint 2', 'Complaint 3']
        })
        self.pipeline.complaints_data = test_data
        
        embeddings = self.pipeline.create_embeddings()
        
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape[0] == 3  # Number of complaints
        assert embeddings.shape[1] == 384  # Embedding dimension

    def test_create_embeddings_invalid_column(self):
        """Test embedding creation with invalid column"""
        # Create test data without the expected column
        test_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B']
        })
        self.pipeline.complaints_data = test_data
        
        embeddings = self.pipeline.create_embeddings()
        
        assert isinstance(embeddings, np.ndarray)
        assert len(embeddings) == 0

    def test_build_vector_store(self):
        """Test vector store building"""
        # Create test data and embeddings
        test_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B'],
            'product': ['Credit Card', 'Mortgage']
        })
        test_embeddings = np.random.rand(2, 384)
        
        self.pipeline.complaints_data = test_data
        
        self.pipeline.build_vector_store(test_embeddings)
        
        assert self.pipeline.vector_store is not None
        assert 'embeddings' in self.pipeline.vector_store
        assert 'metadata' in self.pipeline.vector_store
        assert np.array_equal(self.pipeline.vector_store['embeddings'], test_embeddings)

    def test_search_similar_complaints_no_vector_store(self):
        """Test search when vector store is not built"""
        results = self.pipeline.search_similar_complaints("test query")
        assert results == []

    def test_search_similar_complaints_with_vector_store(self):
        """Test similarity search with vector store"""
        # Set up vector store
        test_metadata = [
            {'company': 'Bank A', 'product': 'Credit Card', 'issue': 'Fraud'},
            {'company': 'Bank B', 'product': 'Mortgage', 'issue': 'Payment'}
        ]
        test_embeddings = np.random.rand(2, 384)
        
        self.pipeline.vector_store = {
            'embeddings': test_embeddings,
            'metadata': test_metadata
        }
        
        results = self.pipeline.search_similar_complaints("credit card fraud", top_k=1)
        
        assert isinstance(results, list)
        assert len(results) == 1
        assert isinstance(results[0], dict)

    def test_run_pipeline(self):
        """Test complete pipeline execution"""
        with patch.object(self.pipeline, 'load_data') as mock_load:
            with patch.object(self.pipeline, 'preprocess_data') as mock_preprocess:
                with patch.object(self.pipeline, 'create_embeddings') as mock_embeddings:
                    with patch.object(self.pipeline, 'build_vector_store') as mock_build:
                        mock_embeddings.return_value = np.random.rand(2, 384)
                        
                        self.pipeline.run_pipeline()
                        
                        mock_load.assert_called_once()
                        mock_preprocess.assert_called_once()
                        mock_embeddings.assert_called_once()
                        mock_build.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__]) 