# Contributing Guide

🎉 **First off, thanks for taking the time to contribute!** 🎉

We welcome contributions from everyone, regardless of experience level. This guide will help you get started with contributing to RAG PDF Chatbot.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Coding Standards](#-coding-standards)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Issue Reporting](#-issue-reporting)
- [Feature Requests](#-feature-requests)

## 🤝 Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainers].

## 🤔 How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/your-org/rag-pdf-chatbot/issues)
- If you're unable to find an open issue addressing the problem, [open a new one](#-issue-reporting)

### Suggesting Enhancements

- Open a new issue with the "enhancement" label
- Provide a clear description of the proposed enhancement
- Explain why this enhancement would be useful

### Writing Code

- Check the [open issues](https://github.com/your-org/rag-pdf-chatbot/issues) for tasks
- Look for issues labeled "good first issue" if you're new
- Comment on the issue to let others know you're working on it

### Improving Documentation

- Fix typos, grammar, or unclear explanations
- Add missing documentation
- Improve existing documentation

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Ollama with required models
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/your-org/rag-pdf-chatbot.git
cd rag-pdf-chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt  # Development dependencies

# Set up pre-commit hooks
pre-commit install
```

### Running the Application

```bash
# Basic test
python -m src.main --help

# Run with sample question
python -m src.main --question "What is RAG?"
```

## 📏 Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://github.com/PyCQA/isort) for import sorting
- Use [flake8](https://flake8.pycqa.org/) for linting

### Type Hints

- Use Python type hints for all functions and methods
- Follow [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hinting guidelines
- Use `Optional` for nullable types
- Use `Any` sparingly

### Documentation

- Follow [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Document all public classes, methods, and functions
- Include examples where helpful
- Keep documentation up-to-date

### Testing

- Write unit tests for new functionality
- Aim for 80%+ code coverage
- Use descriptive test names
- Test edge cases and error conditions

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Examples

```
feat(document_processor): add support for DOCX files

- Added PyMuPDFLoader for DOCX document loading
- Updated chunking strategy for DOCX content
- Added unit tests for DOCX processing

Fixes #123
```

```
fix(vector_store): handle missing vector store gracefully

- Added null checks before vector store operations
- Improved error messages for missing vector store
- Added fallback to rebuild vector store

Closes #456
```

## 🔄 Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies** and set up pre-commit hooks
3. **Make your changes** following coding standards
4. **Write tests** for your changes
5. **Update documentation** if needed
6. **Run tests** to ensure nothing is broken
7. **Commit your changes** with clear commit messages
8. **Push to your fork** and submit a pull request
9. **Wait for review** and address any feedback

### Pull Request Requirements

- Clear title and description
- Reference related issues (e.g., "Fixes #123")
- Pass all CI checks
- Include appropriate tests
- Update documentation if needed
- Follow coding standards

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_document_processor.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v tests/
```

### Test Structure

```
tests/
├── __init__.py
├── test_config.py
├── test_document_processor.py
├── test_vector_store.py
├── test_rag_chain.py
└── test_main.py
```

### Writing Tests

- Use `pytest` framework
- Follow Arrange-Act-Assert pattern
- Test both happy paths and error cases
- Use mocking for external dependencies
- Keep tests focused and fast

## 📚 Documentation

### Documentation Standards

- Use Markdown for all documentation
- Follow consistent formatting
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Use diagrams (Mermaid) for complex concepts

### Documentation Structure

```
docs/
├── ARCHITECTURE.md      # System architecture
├── CONTRIBUTING.md      # Contribution guidelines
├── API.md               # API reference
├── DEPLOYMENT.md        # Deployment guide
└── EXAMPLES.md          # Usage examples
```

## 🐛 Issue Reporting

### Bug Report Template

```markdown
### Description
Clear and concise description of the bug.

### Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Screenshots
If applicable, add screenshots.

### Environment
- OS: [e.g., Windows 10, macOS 12.1, Ubuntu 20.04]
- Python version: [e.g., 3.8.10]
- RAG PDF Chatbot version: [e.g., 1.0.0]

### Additional Context
Add any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
### Problem Statement
Is your feature request related to a problem? Please describe.

### Proposed Solution
Describe the solution you'd like.

### Alternatives
Describe alternatives you've considered.

### Additional Context
Add any other context or screenshots.
```

## 🤝 Community

- Join our [Discord](https://discord.gg/example) for discussions
- Follow us on [Twitter](https://twitter.com/example) for updates
- Star the repository to show your support

## 🙏 Acknowledgments

Thank you to all our contributors who have helped make this project better!

---

**Happy Coding!** 🚀
