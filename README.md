# 🧩 HumorBench

A modern Python project demonstrating best practices for code quality, testing, documentation, and CI/CD.

[![CI](https://github.com/USERNAME/humorbench/workflows/CI/badge.svg)](https://github.com/USERNAME/humorbench/actions)
[![codecov](https://codecov.io/gh/USERNAME/humorbench/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/humorbench)
[![PyPI version](https://badge.fury.io/py/humorbench.svg)](https://badge.fury.io/py/humorbench)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🧪 **Comprehensive Testing**: Full test coverage with pytest
- 🎯 **Type Safety**: Complete type hints and mypy static analysis
- 🧹 **Code Quality**: Automated formatting (Black) and linting (Ruff)
- 📚 **Documentation**: Beautiful docs with MkDocs Material
- 🔄 **CI/CD**: Automated testing and deployment with GitHub Actions
- 📦 **Modern Packaging**: Fast dependency management with uv
- 🚀 **Conventional Commits**: Automated versioning with Commitizen

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/humorbench.git
cd humorbench

# Install dependencies
uv sync

# Run tests
uv run pytest

# Format and lint code
uv run black .
uv run ruff check .

# Type check
uv run mypy src/
```

### Usage

```bash
# Command-line interface
uv run humorbench --help

# Add a joke
uv run humorbench --joke "Why did the chicken cross the road?"

# Calculate humor score
uv run humorbench --score "Why did the chicken cross the road? To get to the other side!"

# Get joke count
uv run humorbench --count
```

## 🏗️ Project Structure

```
humorbench/
├── src/humorbench/       # Main package code
│   ├── __init__.py
│   ├── core.py          # Core functionality
│   └── cli.py           # Command-line interface
├── tests/               # Unit and integration tests
│   ├── test_core.py
│   └── test_cli.py
├── docs/                # Documentation
│   ├── index.md
│   ├── api.md
│   └── contributing.md
├── .github/workflows/   # CI/CD pipelines
├── pyproject.toml       # Project configuration
├── .pre-commit-config.yaml
├── mkdocs.yml          # Documentation config
└── README.md
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=humorbench --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type check
uv run mypy src/

# Install pre-commit hooks
uv run pre-commit install
```

### Documentation

```bash
# Serve docs locally
uv run mkdocs serve

# Build docs
uv run mkdocs build
```

## 📋 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/contributing.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `uv run pytest`
5. Format code: `uv run black .`
6. Lint code: `uv run ruff check .`
7. Type check: `uv run mypy src/`
8. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
9. Push to your fork: `git push origin feature/amazing-feature`
10. Open a Pull Request

## 🛠️ Tools & Technologies

- **[uv](https://docs.astral.sh/uv/)**: Fast Python package manager
- **[pytest](https://pytest.org/)**: Testing framework
- **[Black](https://black.readthedocs.io/)**: Code formatter
- **[Ruff](https://docs.astral.sh/ruff/)**: Fast Python linter
- **[mypy](https://mypy.readthedocs.io/)**: Static type checker
- **[MkDocs](https://www.mkdocs.org/)**: Documentation generator
- **[Commitizen](https://commitizen-tools.github.io/commitizen/)**: Conventional commits
- **[GitHub Actions](https://github.com/features/actions)**: CI/CD

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by modern Python best practices
- Built with ❤️ using open-source tools
- Thanks to all contributors!

---

**Happy coding!** 🎉
