# 📊 DataAnalyzer AI

A powerful, AI-driven data analysis tool with an intuitive web interface. Upload your CSV files and chat with AI to get instant insights, visualizations, and analysis.

![DataAnalyzer AI](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red) ![Google](https://img.shields.io/badge/Google-Gemini%20AI-yellow)

## 🚀 Features

### 🎯 **Simple 3-Step Process**
1. **Upload CSV** - Drag and drop your data file
2. **View Analysis** - Get instant data insights and statistics
3. **Chat with AI** - Ask questions and get visualizations

### 🤖 **AI-Powered Analysis**
- **Natural Language Queries** - Ask questions in plain English
- **Automatic Code Generation** - AI writes Python code for analysis
- **Smart Visualizations** - Creates charts, graphs, and plots automatically
- **Interactive Chat** - Conversational interface for data exploration

### 📊 **Comprehensive Data Analysis**
- **Data Overview** - Rows, columns, missing values, duplicates
- **Statistical Summary** - Descriptive statistics for numeric columns
- **Data Types** - Column information and data types
- **Custom Analysis** - Ask specific questions about your data

### 🎨 **Rich Visualizations**
- **Bar Charts** - Category distributions and comparisons
- **Pie Charts** - Proportional data representation
- **Histograms** - Data distribution analysis
- **Scatter Plots** - Relationship analysis
- **Correlation Heatmaps** - Variable relationships
- **Box Plots** - Statistical distributions
- **Line Charts** - Trend analysis

### 🌐 **Multiple Interfaces**
- **Web App** - Beautiful Streamlit interface
- **Command Line** - Direct CLI interaction
- **Batch Processing** - Automated analysis workflows

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/dataanalyzer-ai.git
cd dataanalyzer-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google Gemini API key
GEMINI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
# Web interface (default)
python main.py

# Command line interface
python main.py --ask data.csv "Show me sales trends"
```

## 🔑 Getting API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 🚀 Usage

### Web Interface

Launch the web application:
```bash
python main.py
```

Then open your browser to `http://localhost:8501`

**Workflow:**
1. **Upload your CSV file**
2. **Review the automatic data analysis**
3. **Start chatting with AI about your data**

**Example questions:**
- "Create a correlation heatmap"
- "Show sales distribution by region"
- "What's the average age by department?"
- "Generate a scatter plot of price vs quantity"
- "Show trends over time"

### Command Line Interface

Direct analysis from command line:
```bash
# Analyze specific question
python main.py --ask data.csv "Create a bar chart of categories"

# Interactive mode
python main.py --interactive data.csv
```

### Batch Processing

Process multiple files or questions:
```bash
# Multiple questions
python main.py --batch data.csv questions.txt

# Multiple files
python main.py --batch-files *.csv "Show summary statistics"
```

## 📁 Project Structure

```
dataanalyzer-ai/
├── main.py                 # Main entry point
├── app.py                  # Streamlit web application
├── data_analyzer.py        # Core analysis engine
├── config.py              # Configuration management
├── csv_handler.py          # Data file handling
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── data/                  # Sample data files
│   └── sample_data.csv
├── output/                # Generated charts and reports
└── temp/                  # Temporary processing files
```

## 🎯 Example Use Cases

### Business Analytics
```
"Show revenue trends by quarter"
"Create a pie chart of customer segments"
"What's the correlation between marketing spend and sales?"
```

### Data Science
```
"Generate a correlation matrix heatmap"
"Show distribution of target variable"
"Create scatter plots for feature relationships"
```

### Research Analysis
```
"Compare groups using box plots"
"Show statistical summary by category"
"Create histograms for all numeric variables"
```

### Financial Analysis
```
"Plot stock price trends"
"Show expense breakdown by category"
"Analyze profit margins over time"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:
```env
GEMINI_API_KEY=your_google_gemini_api_key
MODEL_NAME=gemini-2.5-flash
TIMEOUT_SECONDS=60
MAX_FILE_SIZE_MB=10
```

### Supported File Formats
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Parquet (`.parquet`)

### Output Formats
- PNG images for charts
- CSV files for processed data
- Text reports for analysis

## 🎨 Web Interface Features

### Clean, Minimal Design
- **No distracting colors** - Focus on your data
- **One-page layout** - Everything visible at once
- **Responsive design** - Works on all screen sizes
- **Fast loading** - Optimized for performance

### Smart Chat Interface
- **Conversation history** - See all your questions and answers
- **Inline charts** - Visualizations appear directly in chat
- **Error handling** - Clear error messages and suggestions
- **Auto-save** - Charts saved to output directory

### Data Analysis Dashboard
- **Quick metrics** - Rows, columns, missing values, duplicates
- **Data preview** - First few rows of your dataset
- **Statistical summary** - Descriptive statistics
- **Column information** - Data types and null counts

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```
3. **Make your changes**
4. **Add tests if applicable**
5. **Commit your changes**
```bash
git commit -m "Add amazing feature"
```
6. **Push to your branch**
```bash
git push origin feature/amazing-feature
```
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/dataanalyzer-ai.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 .
black .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful language model capabilities
- **Streamlit** - For the beautiful web interface framework
- **Pandas & NumPy** - For data manipulation and analysis
- **Matplotlib & Seaborn** - For data visualization
- **Python Community** - For the amazing ecosystem

## 🐛 Issues & Support

### Common Issues

**API Key Error:**
```
Error: Please set GEMINI_API_KEY in your .env file
```
**Solution:** Make sure you have a valid Google Gemini API key in your `.env` file.

**File Upload Error:**
```
Error loading file: [details]
```
**Solution:** Check file format (CSV, Excel, JSON, Parquet) and file size (max 10MB).

**Chart Not Displaying:**
```
Error loading image: [details]
```
**Solution:** Check that matplotlib and PIL are installed correctly.

### Getting Help

- **GitHub Issues** - Report bugs and request features
- **Discussions** - Ask questions and share ideas
- **Documentation** - Check this README and code comments

## 🚀 Roadmap

### Upcoming Features
- [ ] **Database Connectivity** - Connect to SQL databases
- [ ] **Advanced ML Models** - Automated machine learning
- [ ] **Dashboard Builder** - Create custom dashboards
- [ ] **Export Options** - PDF reports and presentations
- [ ] **Collaboration** - Share analyses with teams
- [ ] **API Endpoints** - REST API for integration
- [ ] **Docker Support** - Containerized deployment
- [ ] **Cloud Deployment** - One-click cloud hosting

### Version History
- **v1.0.0** - Initial release with web interface and CLI
- **v1.1.0** - Enhanced chart display and bug fixes
- **v1.2.0** - Improved error handling and performance

## 📊 Sample Data

The project includes sample data files in the `data/` directory:

- `sample_data.csv` - Employee data with departments, salaries, performance
- More sample datasets coming soon!

## 🎯 Quick Start Example

1. **Start the web app:**
```bash
python main.py
```

2. **Upload the sample data file**

3. **Try these questions:**
```
"Create a bar chart of department counts"
"Show salary distribution by department"
"Generate a correlation heatmap"
"What's the average performance score?"
```

4. **See instant results with charts and analysis!**

---

**Made with ❤️ for data enthusiasts and analysts everywhere!**

*Transform your data into insights with the power of AI* 🚀📊✨