"""
TrustVoice Analytics Application
Main application for CFPB complaints analysis and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from rag_pipeline import RAGPipeline

# Page configuration
st.set_page_config(
    page_title="TrustVoice Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 TrustVoice Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### Financial Complaints Analysis & Insights Platform")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Complaints Analysis", "RAG Search", "Data Explorer"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Complaints Analysis":
        show_complaints_analysis()
    elif page == "RAG Search":
        show_rag_search()
    elif page == "Data Explorer":
        show_data_explorer()

def show_dashboard():
    """Display the main dashboard"""
    st.header("📊 Dashboard Overview")
    
    # Load data
    try:
        data_path = "data/raw/cfpb_complaints.csv"
        if Path(data_path).exists():
            df = pd.read_csv(data_path)
            st.success(f"✅ Loaded {len(df)} complaints from database")
        else:
            st.warning("⚠️ No data file found. Please upload CFPB complaints data.")
            return
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Complaints", len(df))
    
    with col2:
        if 'company' in df.columns:
            unique_companies = df['company'].nunique()
            st.metric("Unique Companies", unique_companies)
        else:
            st.metric("Unique Companies", "N/A")
    
    with col3:
        if 'product' in df.columns:
            unique_products = df['product'].nunique()
            st.metric("Product Categories", unique_products)
        else:
            st.metric("Product Categories", "N/A")
    
    with col4:
        if 'state' in df.columns:
            unique_states = df['state'].nunique()
            st.metric("States Covered", unique_states)
        else:
            st.metric("States Covered", "N/A")
    
    # Charts
    st.subheader("📈 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'product' in df.columns:
            product_counts = df['product'].value_counts().head(10)
            fig = px.bar(
                x=product_counts.values,
                y=product_counts.index,
                orientation='h',
                title="Top 10 Product Categories",
                labels={'x': 'Number of Complaints', 'y': 'Product'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'state' in df.columns:
            state_counts = df['state'].value_counts().head(10)
            fig = px.bar(
                x=state_counts.values,
                y=state_counts.index,
                orientation='h',
                title="Top 10 States by Complaints",
                labels={'x': 'Number of Complaints', 'y': 'State'}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_complaints_analysis():
    """Display detailed complaints analysis"""
    st.header("🔍 Complaints Analysis")
    
    try:
        df = pd.read_csv("data/raw/cfpb_complaints.csv")
    except:
        st.error("❌ No data available for analysis")
        return
    
    # Analysis options
    analysis_type = st.selectbox(
        "Choose analysis type",
        ["Trend Analysis", "Company Analysis", "Product Analysis", "Geographic Analysis"]
    )
    
    if analysis_type == "Trend Analysis":
        st.subheader("📈 Complaint Trends Over Time")
        if 'date_received' in df.columns:
            df['date_received'] = pd.to_datetime(df['date_received'], errors='coerce')
            monthly_complaints = df.groupby(df['date_received'].dt.to_period('M')).size()
            
            fig = px.line(
                x=monthly_complaints.index.astype(str),
                y=monthly_complaints.values,
                title="Monthly Complaints Trend",
                labels={'x': 'Month', 'y': 'Number of Complaints'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date column not available for trend analysis")
    
    elif analysis_type == "Company Analysis":
        st.subheader("🏢 Company Analysis")
        if 'company' in df.columns:
            company_stats = df['company'].value_counts().head(20)
            
            fig = px.bar(
                x=company_stats.values,
                y=company_stats.index,
                orientation='h',
                title="Top 20 Companies by Complaints",
                labels={'x': 'Number of Complaints', 'y': 'Company'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Company column not available")

def show_rag_search():
    """Display RAG chat interface with answer, sources, and clear functionality"""
    st.header("💬 Chat with TrustVoice RAG")

    # Initialize session state for chat
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'last_answer' not in st.session_state:
        st.session_state['last_answer'] = ''
    if 'last_sources' not in st.session_state:
        st.session_state['last_sources'] = []

    # Input area
    with st.form(key="rag_chat_form", clear_on_submit=False):
        user_query = st.text_input("Type your question:", value="", key="user_query")
        ask_button = st.form_submit_button("Ask")
        clear_button = st.form_submit_button("Clear")

    # Clear chat
    if clear_button:
        st.session_state['chat_history'] = []
        st.session_state['last_answer'] = ''
        st.session_state['last_sources'] = []
        st.experimental_rerun()

    # Handle question submission
    if ask_button and user_query.strip():
        with st.spinner("Retrieving answer..."):
            pipeline = RAGPipeline()
            # Use existing vector store, no need to rebuild
            # Retrieve sources (top_k=5 for context)
            sources = pipeline.search_similar_complaints(user_query, top_k=5)
            st.session_state['last_sources'] = sources
            # Generate answer
            answer = pipeline.generate_answer_with_llm(user_query, top_k=5)
            st.session_state['last_answer'] = answer
            # Add to chat history
            st.session_state['chat_history'].append({
                'question': user_query,
                'answer': answer,
                'sources': sources
            })

    # Display chat history (latest at bottom)
    for entry in st.session_state['chat_history']:
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**TrustVoice RAG:** {entry['answer']}")
        # Show sources
        if entry['sources']:
            with st.expander("Show sources used for this answer"):
                for i, src in enumerate(entry['sources'], 1):
                    st.markdown(f"**Source {i}:** {src.get('document', '')}")
        st.markdown("---")

def show_data_explorer():
    """Display data exploration interface"""
    st.header("📊 Data Explorer")
    
    try:
        df = pd.read_csv("data/raw/cfpb_complaints.csv")
        st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
        
        # Data overview
        st.subheader("📋 Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Data Shape:**", df.shape)
            st.write("**Columns:**", list(df.columns))
        
        with col2:
            st.write("**Missing Values:**")
            missing_data = df.isnull().sum()
            st.write(missing_data[missing_data > 0])
        
        # Data preview
        st.subheader("👀 Data Preview")
        st.dataframe(df.head(10))
        
        # Column analysis
        st.subheader("📈 Column Analysis")
        selected_column = st.selectbox("Select a column to analyze:", df.columns)
        
        if selected_column:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{selected_column} Statistics:**")
                if df[selected_column].dtype in ['int64', 'float64']:
                    st.write(df[selected_column].describe())
                else:
                    st.write(df[selected_column].value_counts().head(10))
            
            with col2:
                if df[selected_column].dtype in ['int64', 'float64']:
                    fig = px.histogram(df, x=selected_column, title=f"Distribution of {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    value_counts = df[selected_column].value_counts().head(10)
                    fig = px.bar(x=value_counts.values, y=value_counts.index, orientation='h',
                               title=f"Top 10 values in {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")

if __name__ == "__main__":
    main() 