# Contributing Guidelines

Thank you for contributing to **HumorBench**!
We follow modern Python best practices for code quality, testing, documentation, and CI/CD.
Please read and follow the guidelines below before submitting your pull request (PR).

---

## 📦 Project Setup

This project uses **[uv](https://docs.astral.sh/uv/)** — a fast Python package manager and build tool.

### 1. Clone and Install
```bash
git clone https://github.com/USERNAME/humorbench.git
cd humorbench
uv sync
```

### 2. Run Tests
```bash
uv run pytest
```

### 3. Format, Lint, and Type Check
```bash
uv run black .
uv run ruff check .
uv run mypy src/
```

## 🧱 Project Structure

```
humorbench/
├── src/humorbench/       # Main package code
├── tests/               # Unit and integration tests
├── docs/                # Documentation (MkDocs)
├── pyproject.toml       # Project configuration
├── .pre-commit-config.yaml
└── README.md
```

All code must live inside `src/` (no top-level imports).
This ensures cleaner import paths and avoids name conflicts.

## 🧪 Testing & Coverage

We use pytest for testing.

- Include tests for every new feature or bugfix.
- Maintain ≥ 85% coverage (enforced via CI).

Run coverage locally:

```bash
uv run pytest --cov=humorbench --cov-report=term-missing
```

## 🧠 Type Hints & Static Analysis

All new code must include type annotations (Python ≥3.10 syntax).

Static type checking is enforced via mypy.

Follow the PEP 484 and PEP 561 standards.

```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

## 🧹 Code Quality

### Formatting
We use Black for code formatting (line length = 88).

Run it automatically before committing:

```bash
uv run black .
```

### Linting
We use Ruff (combines flake8, isort, pylint).

Run linting:

```bash
uv run ruff check .
```

### Pre-commit Hooks
Install and enable:

```bash
uv run pre-commit install
```

## 🧾 Conventional Commits

All commits must follow the Conventional Commits format:

```
feat: add new user profile endpoint
fix: correct auth token refresh logic
docs: update API usage section
```

### Automating Version Bumps
Use Commitizen:

```bash
uv run cz bump
```

## 📘 Documentation

All new code must be documented:

- Include docstrings for all public functions, classes, and modules.
- Follow the Google or NumPy docstring style.
- Update project-level docs in README.md or the documentation site (MkDocs)

### Build Docs
```bash
uv run mkdocs serve
```

Docs will auto-deploy via CI on merges to main.

## 🔄 CI/CD Pipeline

Our GitHub Actions CI runs:

- Lint (ruff, black)
- Type checking (mypy)
- Unit tests + coverage
- Docs build check

## 🔒 Branch Protection

PRs to main require:

- ✅ All CI checks passing
- ✅ At least one reviewer approval

Direct pushes to main are disallowed.

## ⚙️ Dependencies & Environments

Dependencies are grouped in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["black", "ruff", "mypy", "pytest", "pytest-cov", "commitizen"]
docs = ["mkdocs", "mkdocs-material", "mkdocstrings"]
```

Use `uv lock` for reproducible builds.

Keep secrets/configs in `.env` files or environment variables (not in code).

## 🧪 Test-Driven Development (TDD)

We strongly encourage TDD:

1. Write tests first.
2. Implement minimal code to pass them.
3. Refactor while keeping tests green.

## 🚀 Releasing

Bump version with Commitizen:

```bash
uv run cz bump
```

Tag and push:

```bash
git push --tags
```

GitHub Action will publish to PyPI using:

```bash
uv publish
```

## 🎯 Summary Checklist Before PR

- [ ] Code formatted with Black
- [ ] Lint passes with Ruff
- [ ] All tests pass (pytest)
- [ ] ≥85% coverage
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] Commit message follows Conventional Commits
