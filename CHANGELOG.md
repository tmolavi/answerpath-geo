# Changelog

All notable changes to AnswerPath GEO are documented here.

## [v0.2.0] - 2026-10-14
### Added
- **Authentic AI Conversational Query Simulation**: Overhauled prompt generation engine to model real human queries asked to ChatGPT, Perplexity, Claude, and Gemini rather than rigid search keywords.
- **Multimodal & Vision AI Queries**: Added simulation for image/screenshot queries (competitor UI audit, quotation analysis, Search Console drop diagnostics, pricing matrices) with rich `image_context`.
- **Voice Dictation & Spoken Assistant Queries**: Added conversational voice queries featuring natural spoken preambles and colloquial phrasing (`voice_markers`).
- **Target Website & URL Extraction**: Added automatic domain and URL ingestion (`--url` or passing a domain/URL) to extract brand, title, headings, and offerings to tailor competitive queries.
- **Rich Persona & Funnel Stratification**: Tagged queries by persona (`business_owner`, `technical_buyer`, `skeptical_customer`, `marketing_lead`, `budget_conscious_buyer`) and acquisition stage (`awareness`, `consideration`, `decision`, `retention`).
- **Direct GEO-Scope Benchmark Compatibility**: Generates structured prompt records matching `BENCHMARK_ECOSYSTEM.md` (`benchmark_prompts.json`).
- **CLI & Module Execution**: Added `answerpath_geo/__main__.py` allowing `python3 -m answerpath_geo`. Added `--url`, `--modality`, `--lang`, `--count`, and `--benchmark` flags.
- **Badges**: Added PyPI version, Python versions, and MIT license badges to README and multilingual guides.

### Changed
- Refactored `models.py`, `extractor.py`, `generator.py`, and `core.py` while ensuring 100% backward compatibility for legacy properties (`text`, `evidence`, `intent`, `stage`, `frequency`, `cluster`).
- Enhanced MCP server schema with `url`, `modality`, `lang`, `count`, and `benchmark_format`.

## [v2026.1.1] - 2026-09-18
### Added
- Standardized runnable examples (`examples/sample_queries.json`, `examples/discover_example.py`).
- Automated GitHub Actions CI workflow across Python 3.10, 3.11, 3.12.
- Issue and pull request contribution templates.
- Explicit ecosystem navigation links and data contracts.

## [v2026.1.0] - 2026-09-17
### Added
- Question Discovery & Intent Stratification Layer for GEO-Scope Benchmark 2026.1.
- Strict demand provenance separation (`source_type: "observed"` vs `"generated"`).
- 5 intent categories: `commercial`, `compare`, `trust`, `solve`, `buy`.
- FastMCP stdio and HTTP server interfaces.
