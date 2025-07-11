"""
Unit tests for the Streamlit app
"""

import pytest
import pandas as pd
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Mock streamlit for testing
import streamlit as st
st.set_page_config = MagicMock()
st.markdown = MagicMock()
st.sidebar = MagicMock()
st.columns = MagicMock()
st.metric = MagicMock()
st.subheader = MagicMock()
st.plotly_chart = MagicMock()
st.text_input = MagicMock()
st.slider = MagicMock()
st.button = MagicMock()
st.spinner = MagicMock()
st.success = MagicMock()
st.warning = MagicMock()
st.error = MagicMock()
st.expander = MagicMock()
st.write = MagicMock()
st.dataframe = MagicMock()
st.selectbox = MagicMock()

# Mock plotly
import plotly.express as px
px.bar = MagicMock()
px.line = MagicMock()
px.histogram = MagicMock()

# Mock the app functions
with patch('streamlit.set_page_config'):
    with patch('streamlit.markdown'):
        with patch('streamlit.sidebar'):
            with patch('streamlit.columns'):
                with patch('streamlit.metric'):
                    with patch('streamlit.subheader'):
                        with patch('streamlit.plotly_chart'):
                            with patch('streamlit.text_input'):
                                with patch('streamlit.slider'):
                                    with patch('streamlit.button'):
                                        with patch('streamlit.spinner'):
                                            with patch('streamlit.success'):
                                                with patch('streamlit.warning'):
                                                    with patch('streamlit.error'):
                                                        with patch('streamlit.expander'):
                                                            with patch('streamlit.write'):
                                                                with patch('streamlit.dataframe'):
                                                                    with patch('streamlit.selectbox'):
                                                                        with patch('plotly.express.bar'):
                                                                            with patch('plotly.express.line'):
                                                                                with patch('plotly.express.histogram'):
                                                                                    from app import main, show_dashboard, show_complaints_analysis, show_rag_search, show_data_explorer


class TestStreamlitApp:
    """Test cases for Streamlit app functions"""

    def setup_method(self):
        """Set up test fixtures"""
        # Reset all mocks
        for mock in [st.set_page_config, st.markdown, st.sidebar, st.columns, 
                    st.metric, st.subheader, st.plotly_chart, st.text_input,
                    st.slider, st.button, st.spinner, st.success, st.warning,
                    st.error, st.expander, st.write, st.dataframe, st.selectbox]:
            mock.reset_mock()

    @patch('pandas.read_csv')
    def test_show_dashboard_with_data(self, mock_read_csv):
        """Test dashboard with valid data"""
        # Mock data
        mock_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B', 'Bank C'],
            'product': ['Credit Card', 'Mortgage', 'Student Loan'],
            'state': ['CA', 'NY', 'TX']
        })
        mock_read_csv.return_value = mock_data
        
        # Mock Path.exists to return True
        with patch('pathlib.Path.exists', return_value=True):
            show_dashboard()
        
        # Verify that success message was called
        st.success.assert_called()

    @patch('pandas.read_csv')
    def test_show_dashboard_no_data(self, mock_read_csv):
        """Test dashboard with no data file"""
        # Mock Path.exists to return False
        with patch('pathlib.Path.exists', return_value=False):
            show_dashboard()
        
        # Verify that warning message was called
        st.warning.assert_called()

    @patch('pandas.read_csv')
    def test_show_complaints_analysis(self, mock_read_csv):
        """Test complaints analysis page"""
        # Mock data
        mock_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B'],
            'product': ['Credit Card', 'Mortgage'],
            'date_received': ['2023-01-01', '2023-01-02']
        })
        mock_read_csv.return_value = mock_data
        
        show_complaints_analysis()
        
        # Verify that selectbox was called for analysis type selection
        st.selectbox.assert_called()

    def test_show_rag_search(self):
        """Test RAG search functionality"""
        # Mock text input to return a query
        st.text_input.return_value = "credit card fraud"
        st.button.return_value = True
        
        # Mock the RAG pipeline
        with patch('app.RAGPipeline') as mock_rag:
            mock_pipeline = MagicMock()
            mock_rag.return_value = mock_pipeline
            mock_pipeline.search_similar_complaints.return_value = [
                {'company': 'Bank A', 'product': 'Credit Card', 'issue': 'Fraud'}
            ]
            
            show_rag_search()
        
        # Verify that search was initiated
        st.button.assert_called()

    @patch('pandas.read_csv')
    def test_show_data_explorer(self, mock_read_csv):
        """Test data explorer functionality"""
        # Mock data
        mock_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B'],
            'product': ['Credit Card', 'Mortgage'],
            'state': ['CA', 'NY']
        })
        mock_read_csv.return_value = mock_data
        
        show_data_explorer()
        
        # Verify that success message was called
        st.success.assert_called()

    def test_main_function(self):
        """Test main app function"""
        # Mock sidebar selectbox to return a page
        st.sidebar.selectbox.return_value = "Dashboard"
        
        # Mock the page functions
        with patch('app.show_dashboard') as mock_dashboard:
            main()
            mock_dashboard.assert_called_once()

    @patch('pandas.read_csv')
    def test_dashboard_metrics(self, mock_read_csv):
        """Test dashboard metrics calculation"""
        # Mock data with all required columns
        mock_data = pd.DataFrame({
            'company': ['Bank A', 'Bank B', 'Bank C'],
            'product': ['Credit Card', 'Mortgage', 'Student Loan'],
            'state': ['CA', 'NY', 'TX'],
            'date_received': ['2023-01-01', '2023-01-02', '2023-01-03']
        })
        mock_read_csv.return_value = mock_data
        
        # Mock Path.exists to return True
        with patch('pathlib.Path.exists', return_value=True):
            show_dashboard()
        
        # Verify that metrics were calculated
        assert st.metric.call_count >= 4  # At least 4 metrics should be called

    def test_rag_search_no_query(self):
        """Test RAG search with no query"""
        # Mock text input to return empty string
        st.text_input.return_value = ""
        st.button.return_value = True
        
        show_rag_search()
        
        # Verify that warning was shown for empty query
        st.warning.assert_called()

    @patch('pandas.read_csv')
    def test_complaints_analysis_trend(self, mock_read_csv):
        """Test trend analysis in complaints analysis"""
        # Mock data with date column
        mock_data = pd.DataFrame({
            'date_received': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'company': ['Bank A', 'Bank B', 'Bank C']
        })
        mock_read_csv.return_value = mock_data
        
        # Mock selectbox to return "Trend Analysis"
        st.selectbox.return_value = "Trend Analysis"
        
        show_complaints_analysis()
        
        # Verify that trend analysis was attempted
        st.subheader.assert_called()


if __name__ == "__main__":
    pytest.main([__file__]) 