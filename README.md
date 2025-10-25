# HumorBench

[FILL IN DESCRIPTION HERE]

## Quick Start

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

## Project Structure

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

## Development

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
