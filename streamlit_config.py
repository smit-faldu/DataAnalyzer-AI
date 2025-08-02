"""
Streamlit configuration and helper functions
"""

import streamlit as st
from pathlib import Path

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="DataAnalyzer AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/dataanalyzer',
            'Report a bug': 'https://github.com/your-repo/dataanalyzer/issues',
            'About': """
            # DataAnalyzer AI
            
            An AI-powered data analysis tool that converts your CSV files into insights!
            
            **Features:**
            - Upload CSV, Excel, JSON files
            - AI-powered analysis with Gemini
            - Interactive visualizations
            - Data quality assessment
            - Export results
            
            Built with Streamlit and AutoGen.
            """
        }
    )

def load_custom_css():
    """Load custom CSS styling"""
    css = """
    <style>
        /* Main header styling */
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Sub-header styling */
        .sub-header {
            font-size: 1.5rem;
            color: #ff7f0e;
            margin-bottom: 1rem;
            border-bottom: 2px solid #ff7f0e;
            padding-bottom: 0.5rem;
        }
        
        /* Success message box */
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Error message box */
        .error-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Info message box */
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 0.5rem;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* File upload area */
        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            background-color: #f9f9f9;
            margin: 1rem 0;
        }
        
        /* Question buttons */
        .question-btn {
            background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
            border: none;
            border-radius: 3px;
            color: white;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .question-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Analysis history */
        .history-item {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
        }
        
        /* Data preview table */
        .dataframe {
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Loading spinner */
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        
        /* Chart containers */
        .chart-container {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 3rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_sample_questions():
    """Create a list of sample questions for different data types"""
    return {
        "General Analysis": [
            "Show me basic statistics for this dataset",
            "Perform comprehensive exploratory data analysis",
            "Create a data quality report with recommendations",
            "Generate a summary report of key findings"
        ],
        "Visualizations": [
            "Create visualizations for all numeric columns",
            "Make a correlation heatmap of numeric variables",
            "Show distribution plots for categorical variables",
            "Create scatter plots showing relationships between variables"
        ],
        "Business Insights": [
            "Identify patterns and trends in the data",
            "Find outliers and anomalies",
            "Compare groups by categorical variables",
            "Analyze performance metrics and KPIs"
        ],
        "Advanced Analysis": [
            "Perform clustering analysis on the data",
            "Create predictive models if applicable",
            "Identify the most important features",
            "Generate actionable business recommendations"
        ]
    }

def display_welcome_message():
    """Display welcome message and instructions"""
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Welcome to DataAnalyzer AI!</h3>
        <p>Transform your data into insights with AI-powered analysis:</p>
        <ul>
            <li>📊 <strong>Upload</strong> your CSV, Excel, or JSON file</li>
            <li>🤖 <strong>Ask questions</strong> about your data in natural language</li>
            <li>📈 <strong>Get visualizations</strong> and insights automatically</li>
            <li>💾 <strong>Download results</strong> for further use</li>
        </ul>
        <p><em>Powered by Gemini AI and built from your Jupyter notebook!</em></p>
    </div>
    """, unsafe_allow_html=True)

def display_feature_highlights():
    """Display feature highlights"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI-Powered</h4>
            <p>Gemini AI analyzes your data and generates insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Multi-Format</h4>
            <p>CSV, Excel, JSON, Parquet support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Interactive</h4>
            <p>Real-time visualizations and analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>🔍 Quality Checks</h4>
            <p>Automatic data validation and recommendations</p>
        </div>
        """, unsafe_allow_html=True)

def create_footer():
    """Create application footer"""
    st.markdown("""
    <div class="footer">
        <p>🚀 <strong>DataAnalyzer AI</strong> - From Jupyter Notebook to Production Web App</p>
        <p>Built with ❤️ using Streamlit, AutoGen, and Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)