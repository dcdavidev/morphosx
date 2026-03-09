# Contributing to morphosx 🧬

First off, thank you for considering contributing to MorphosX! It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

## 🚀 Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/morphosx.git
    cd morphosx
    ```
3.  **Install dependencies** using uv:
    ```bash
    uv sync --all-extras
    ```
4.  **Install Lefthook** for automated hooks:
    ```bash
    uv run lefthook install
    ```
4.  **Set up your environment**: Create a `.env` file based on the examples in the README.

## 🛠️ Development Workflow

We follow a strict workflow to maintain high code quality and automated versioning.

### 1. Conventional Commits

We use **Conventional Commits** to automate our changelog and versioning. Instead of using `git commit`, please use our interactive wizard:

```bash
uv run poe commit
```

This will guide you through creating a valid commit message (e.g., `feat: ...`, `fix: ...`, `docs: ...`).

### 2. Automation Tasks

We use `poethepoet` to simplify common tasks. Here are the most relevant ones:

- `uv run poe check`: Runs the full test suite. **Always run this before submitting a PR.**
- `uv run poe clean`: Clears the local image cache.
- `uv run poe commit`: The interactive commit wizard.

### 3. Code Style

- We use **Ruff** for both formatting and linting.
- Please ensure your code follows these standards (enforced by Lefthook) before submitting.

## 🧪 Testing

All new features or bug fixes must include tests. We use `pytest`.

```bash
uv run poe check
```

## 📥 Pull Request Process

1.  Create a new branch for your feature or fix: `git checkout -b feat/my-awesome-feature`.
2.  Make your changes and ensure tests pass.
3.  Commit using `uv run poe commit`.
4.  Push to your fork and submit a **Pull Request**.
5.  Clearly describe the changes and link to any relevant issues.

## 📦 Versioning

Versions are managed automatically by the maintainers using:

```bash
uv run poe release
```

_Note: Do not manually update the version in `pyproject.toml` or `CHANGELOG.md` in your PR._

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's **MIT License**.
