# Contributing to DataAnalyzer AI

Thank you for your interest in contributing to DataAnalyzer AI! We welcome contributions from the community and are excited to see what you'll bring to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Google Gemini API key

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/dataanalyzer-ai.git
   cd dataanalyzer-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   ```

5. **Test the setup**
   ```bash
   python main.py --web
   ```

## 🎯 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **🐛 Bug Reports** - Help us identify and fix issues
- **✨ Feature Requests** - Suggest new functionality
- **📝 Documentation** - Improve docs, examples, tutorials
- **🔧 Code Contributions** - Bug fixes, new features, optimizations
- **🧪 Testing** - Add tests, improve test coverage
- **🎨 UI/UX Improvements** - Enhance the web interface

### Before You Start

1. **Check existing issues** - Look for similar bug reports or feature requests
2. **Create an issue** - Discuss your idea before starting work
3. **Get feedback** - Make sure your contribution aligns with project goals

## 📋 Development Guidelines

### Code Style

We follow Python best practices:

- **PEP 8** - Python style guide
- **Type hints** - Use type annotations where possible
- **Docstrings** - Document functions and classes
- **Comments** - Explain complex logic

Example:
```python
def analyze_data(df: pd.DataFrame, question: str) -> Dict[str, Any]:
    """
    Analyze data based on user question.
    
    Args:
        df: Input DataFrame
        question: User's analysis question
        
    Returns:
        Dictionary containing analysis results
    """
    # Implementation here
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add correlation heatmap visualization"
git commit -m "Fix chart display issue in web interface"
git commit -m "Update README with installation instructions"

# Avoid
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

### Branch Naming

Use descriptive branch names:

```bash
# Features
git checkout -b feature/add-database-support
git checkout -b feature/improve-chart-rendering

# Bug fixes
git checkout -b fix/streamlit-upload-error
git checkout -b fix/memory-leak-in-analyzer

# Documentation
git checkout -b docs/update-api-reference
git checkout -b docs/add-examples
```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run the web app
python main.py --web

# Test CLI functionality
python main.py --ask data/sample_data.csv "test question"

# Run tests (if available)
python -m pytest tests/
```

### 4. Commit and Push

```bash
git add .
git commit -m "Add your descriptive commit message"
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

- Go to GitHub and create a pull request
- Provide a clear description of your changes
- Link any related issues
- Wait for review and feedback

## 🧪 Testing

### Manual Testing

Before submitting, test these scenarios:

1. **Web Interface**
   - Upload different file formats (CSV, Excel, JSON)
   - Try various analysis questions
   - Check chart generation and display
   - Test error handling

2. **Command Line**
   - Test CLI commands
   - Verify output files are generated
   - Check error messages

3. **Edge Cases**
   - Large files
   - Files with missing data
   - Invalid file formats
   - Network connectivity issues

### Automated Testing

If you're adding tests:

```bash
# Create test files in tests/ directory
tests/
├── test_data_analyzer.py
├── test_csv_handler.py
└── test_web_interface.py

# Run tests
python -m pytest tests/ -v
```

## 📝 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include type hints
- Comment complex algorithms
- Update README if needed

### User Documentation

- Update README for new features
- Add examples for new functionality
- Create tutorials for complex features
- Update API documentation

## 🐛 Bug Reports

When reporting bugs, include:

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Upload file '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- Browser: [e.g. Chrome 96, Firefox 95]

**Additional context**
Any other context about the problem.
```

## ✨ Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context, mockups, or examples.
```

## 🎯 Priority Areas

We're especially interested in contributions for:

### High Priority
- **Performance optimizations** - Faster data processing
- **New chart types** - Additional visualization options
- **Error handling** - Better error messages and recovery
- **Mobile responsiveness** - Improve mobile web experience

### Medium Priority
- **Database connectivity** - Support for SQL databases
- **Export features** - PDF reports, PowerPoint slides
- **Advanced analytics** - Statistical tests, ML models
- **Collaboration features** - Sharing and commenting

### Nice to Have
- **Themes and customization** - UI customization options
- **Plugin system** - Extensible architecture
- **Real-time data** - Live data streaming
- **Multi-language support** - Internationalization

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Respect different viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Collaborative
- Help others learn and grow
- Share knowledge and resources
- Provide constructive feedback
- Celebrate others' contributions

### Be Professional
- Keep discussions on-topic
- Avoid personal attacks or harassment
- Follow the code of conduct
- Maintain a professional tone

## 📞 Getting Help

### Questions and Support

- **GitHub Discussions** - General questions and ideas
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Check README and code comments

### Contact

- **Project Maintainers** - Tag @maintainers in issues
- **Community** - Join discussions and help others

## 🏆 Recognition

Contributors will be recognized in:

- **README.md** - Contributors section
- **Release notes** - Feature acknowledgments
- **GitHub** - Contributor badges and stats

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to DataAnalyzer AI! 🚀📊✨**