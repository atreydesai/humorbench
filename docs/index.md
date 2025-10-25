# HumorBench

A modern Python project demonstrating best practices for code quality, testing, documentation, and CI/CD.

## Features

- 🧪 Comprehensive test coverage with pytest
- 🎯 Type hints and static analysis with mypy
- 🧹 Code formatting with Black and linting with Ruff
- 📚 Documentation with MkDocs
- 🔄 CI/CD pipeline with GitHub Actions
- 📦 Modern Python packaging with uv

## Quick Start

### Installation

```bash
git clone https://github.com/USERNAME/humorbench.git
cd humorbench
uv sync
```

### Usage

```bash
# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .

# Type check
uv run mypy src/

# Run the CLI
uv run humorbench --help
```

## Development

This project follows modern Python best practices:

- **Type hints**: All code includes comprehensive type annotations
- **Testing**: Maintains ≥85% test coverage
- **Code quality**: Automated formatting, linting, and type checking
- **Documentation**: Comprehensive docs with MkDocs
- **CI/CD**: Automated testing and deployment

## Contributing

Please read our [Contributing Guidelines](contributing.md) before submitting pull requests.

## License

MIT License - see LICENSE file for details.
