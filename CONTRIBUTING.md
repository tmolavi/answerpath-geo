# Contributing to AnswerPath GEO

We welcome issues and pull requests from the community!

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tmolavi/answerpath-geo.git
   cd answerpath-geo
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   pip install pytest
   ```
3. Run tests:
   ```bash
   pytest tests/ -v
   ```

## Pull Request Guidelines

- Ensure all existing unit tests pass.
- Maintain strict separation between observed user demand and generated prompt templates.
- Follow Conventional Commits format (`feat: ...`, `fix: ...`, `docs: ...`).
- Never submit hardcoded credentials or private conversation logs.
