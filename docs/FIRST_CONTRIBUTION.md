# First Contribution Guide: AnswerPath GEO

Welcome to AnswerPath GEO! We welcome contributions to our question discovery algorithms, search query clustering, and epistemic demand stratification layers.

---

## ⚡ 5-Step Contributor Journey

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/tmolavi/answerpath-geo.git
   cd answerpath-geo
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Run Tests & Demo**:
   ```bash
   pytest tests/ -v
   python examples/public_demo/run_demo.py
   ```

3. **Open Issue / Discussion**: Check [GitHub Discussions](https://github.com/tmolavi/answerpath-geo/discussions) or open a structured issue.
4. **Implement Changes**: Branch from `main`, follow type annotations, add unit tests.
5. **Submit Pull Request**: Open a PR with clear problem context and passing CI tests.

---

## 🎯 Contribution Opportunities
- Query clustering and deduplication heuristics (`answerpath_geo/cluster.py`).
- Additional export format parsers (CSV, JSONL, logs).
- Stratified prompt generation templates.
