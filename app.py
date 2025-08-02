"""
Minimal DataAnalyzer AI - Streamlit Web Application
Simple, clean interface with no infinity loops
"""

import streamlit as st
import pandas as pd
import numpy as np
import asyncio
import tempfile
import os
import sys
from pathlib import Path
from PIL import Image
from datetime import datetime

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from data_analyzer import DataAnalyzer
from config import config
from csv_handler import DataFileHandler

# Page configuration
st.set_page_config(
    page_title="DataAnalyzer AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS - No colors
st.markdown("""
<style>
    .main-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        border: 1px solid #ddd;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .analysis-section {
        border: 1px solid #ddd;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .chat-section {
        border: 1px solid #ddd;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .chat-message {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ddd;
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'processed_images' not in st.session_state:
        st.session_state.processed_images = set()

def load_data_file(uploaded_file):
    """Load data from uploaded file"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Load data using DataFileHandler
        handler = DataFileHandler()
        df, metadata = handler.load_data(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return df, metadata, None
    except Exception as e:
        return None, None, str(e)

def show_data_analysis(df):
    """Show basic data analysis"""
    st.markdown("### 📊 Data Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("Duplicates", df.duplicated().sum())
    
    # Data preview
    st.markdown("**Data Preview:**")
    st.dataframe(df.head(), use_container_width=True)
    
    # Basic statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.markdown("**Numeric Columns Summary:**")
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    # Column info
    st.markdown("**Column Information:**")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str),
        'Non-Null': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(col_info, use_container_width=True)

async def process_question(analyzer, question):
    """Process AI question"""
    try:
        # Get existing images before processing
        existing_files = set(analyzer.list_output_files())
        
        # Process the question
        result = await analyzer.ask_agent(question, execute_code=True)
        
        # Get only newly generated images
        all_files = set(analyzer.list_output_files())
        new_files = all_files - existing_files
        new_image_files = [f for f in new_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        return result, new_image_files
    except Exception as e:
        return {'success': False, 'error': str(e)}, []

def display_chat_message(role, content, images=None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f'<div class="chat-message"><strong>You:</strong> {content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message"><strong>AI:</strong> {content}</div>', unsafe_allow_html=True)
        
        # Display images if any
        if images:
            for img_path in images:
                try:
                    if os.path.exists(img_path):
                        img = Image.open(img_path)
                        st.image(img, caption=Path(img_path).name, use_column_width=True)
                        st.markdown(f"📊 **Chart Generated:** {Path(img_path).name}")
                    else:
                        st.warning(f"Chart file not found: {img_path}")
                except Exception as e:
                    st.error(f"Error loading image {Path(img_path).name}: {str(e)}")

def main():
    """Main application - All in one page"""
    init_session_state()
    
    # Title
    st.markdown('<h1 class="main-title">DataAnalyzer AI</h1>', unsafe_allow_html=True)
    
    # 1. Upload CSV Section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 1. Upload CSV File")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your CSV file to start analysis"
    )
    
    if uploaded_file is not None and not st.session_state.data_loaded:
        with st.spinner("Loading data..."):
            df, metadata, error = load_data_file(uploaded_file)
            
            if error:
                st.error(f"Error loading file: {error}")
            else:
                # Initialize analyzer
                if not config.gemini_api_key:
                    st.error("Please set GEMINI_API_KEY in your .env file")
                    return
                
                try:
                    analyzer = DataAnalyzer()
                    result = analyzer.load_data_from_dataframe(df, uploaded_file.name)
                    
                    if result['success']:
                        st.session_state.analyzer = analyzer
                        st.session_state.data = df
                        st.session_state.data_loaded = True
                        st.success("Data loaded successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result['error']}")
                except Exception as e:
                    st.error(f"Error initializing analyzer: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Data Analysis Section (only show if data is loaded)
    if st.session_state.data_loaded and st.session_state.data is not None:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("### 2. Data Analysis")
        show_data_analysis(st.session_state.data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. Chat Section
        st.markdown('<div class="chat-section">', unsafe_allow_html=True)
        st.markdown("### 3. Chat with AI")
        
        # Display chat history
        for message in st.session_state.chat_history:
            display_chat_message(
                message['role'], 
                message['content'], 
                message.get('images', [])
            )
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            question = st.text_input(
                "Ask a question about your data:",
                placeholder="e.g., 'Create a correlation heatmap' or 'Show sales trends'"
            )
            col1, col2 = st.columns([1, 5])
            
            with col1:
                submit = st.form_submit_button("Send")
            with col2:
                if st.form_submit_button("Reset Data"):
                    st.session_state.analyzer = None
                    st.session_state.data = None
                    st.session_state.chat_history = []
                    st.session_state.data_loaded = False
                    st.session_state.processed_images = set()
                    st.rerun()
        
        # Process question
        if submit and question and not st.session_state.processing:
            st.session_state.processing = True
            
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question,
                'images': []
            })
            
            # Process with AI
            with st.spinner("AI is analyzing..."):
                try:
                    result, image_files = asyncio.run(
                        process_question(st.session_state.analyzer, question)
                    )
                    
                    if result['success']:
                        ai_response = result.get('response', 'Analysis completed!')
                        
                        # Add AI response to history
                        st.session_state.chat_history.append({
                            'role': 'ai',
                            'content': ai_response,
                            'images': image_files
                        })
                        
                        # Copy outputs
                        st.session_state.analyzer.copy_outputs_to_output_dir()
                    else:
                        st.session_state.chat_history.append({
                            'role': 'ai',
                            'content': f"Error: {result.get('error', 'Unknown error')}",
                            'images': []
                        })
                
                except Exception as e:
                    st.session_state.chat_history.append({
                        'role': 'ai',
                        'content': f"Error: {str(e)}",
                        'images': []
                    })
            
            st.session_state.processing = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
