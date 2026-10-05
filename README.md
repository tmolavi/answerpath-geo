# AnswerPath GEO — Discover the Questions People Ask AI Before They Find Your Business

**AnswerPath GEO** is a privacy-first, open-source **SEO, GEO and AEO question mining engine**. Give it a business, service, website topic or keyword and it builds a transparent question map showing what people may ask an AI assistant before choosing a provider.

It separates **observed questions** extracted from exports and application logs from **generated research prompts**. This distinction matters: generated prompts are hypotheses, not evidence of what people actually asked.

**Languages:** [فارسی](README.fa.md) · [Türkçe](README.tr.md) · [Azərbaycan dili](README.az.md) · [العربية](README.ar.md)

**Try it:** [PyPI package](https://pypi.org/project/answerpath-geo/) · [Hugging Face demo](https://huggingface.co/spaces/taqimolavi/answerpath-geo)

## شروع خیلی ساده (برای تیم)

AnswerPath فقط یک کار انجام می‌دهد: از نام کسب‌وکار یا موضوع شما، فهرستی از سؤال‌هایی می‌سازد که می‌توانند برای FAQ، مقاله، صفحه خدمات و تحقیق GEO استفاده شوند.

### آیا سرویس خارجی یا کلید API می‌خواهد؟

خیر. برای حالت معمول، فقط Python 3.10 یا جدیدتر لازم است. ابزار به ChatGPT، Claude، گوگل یا هیچ حسابی وارد نمی‌شود و فایل‌های شما را به جایی نمی‌فرستد.

### سریع‌ترین استفاده

```bash
pip install answerpath-geo
answerpath "مشاوره سئو برای فروشگاه اینترنتی"
```

دو فایل در پوشه‌ی `answerpath-output/` ساخته می‌شود: `questions.json` برای پردازش ماشینی و `questions.csv` برای باز کردن در Excel یا Google Sheets.

### خروجی را چطور بخوانیم؟

- `observed`: سؤال واقعاً در فایل ورودی شما دیده شده است.
- `generated`: سؤال پیشنهادی ابزار است؛ به معنی تقاضای واقعی نیست.
- `intent` و `stage`: نشان می‌دهند کاربر دنبال یادگیری، مقایسه، خرید یا اعتمادسازی بوده و در کدام مرحله قرار دارد.

اگر هنوز فایل مکالمه یا لاگ ندارید، فقط نام موضوع را بدهید. اگر داده‌ی واقعی دارید، آن را با `--input` اضافه کنید. برای حفظ حریم خصوصی، از فایل‌های ناشناس‌سازی‌شده استفاده کنید.

### اگر فقط سؤال‌های واقعی را می‌خواهید

```bash
answerpath "خدمات سئو" --input ./support.json --no-generated
```

### اگر خطا دیدید

اول این دو مورد را بررسی کنید: Python شما باید 3.10+ باشد و نصب باید در همان محیطی انجام شود که دستور `answerpath` را اجرا می‌کنید. این ابزار برای اجرای محلی به Hugging Face یا ZeroGPU وابسته نیست. [راهنمای کامل فارسی](README.fa.md) را هم ببینید.

[Installation](#installation) · [Quick start](#quick-start) · [Inputs](#supported-inputs) · [Outputs](#outputs) · [GEO/AEO method](#geo-and-aeo-method) · [Privacy](#privacy-and-data-boundaries) · [Integrations](#integrations)

**MCP clients:** [Codex, Antigravity, Claude, Cursor and Cloud setup](#mcp-setup)

## Why AnswerPath GEO?

Traditional keyword tools show phrases typed into search engines. AI assistants receive longer, conversational questions: “Which agency is reliable for…?”, “What should I compare…?”, and “Is this service worth the price?”. AnswerPath turns the questions you already own into a usable **answer-path map** for content, FAQ, schema and AI visibility research.

It is designed for marketers, publishers, agencies and product teams who need to:

- discover and normalize user questions from ChatGPT, Claude, Codex, Antigravity, Cursor and chatbot exports;
- group questions by intent and decision stage;
- identify recurring questions without silently inventing demand;
- create an auditable prompt bank for GEO/AEO experiments;
- keep private conversation data on the operator’s machine.

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/tmolavi/answerpath-geo.git
cd answerpath-geo
python3 -m venv .venv
.venv/bin/pip install -e .
```

## PyPI publishing

The stable package is available at [PyPI](https://pypi.org/project/answerpath-geo/).
Future releases are published from GitHub Actions through Trusted Publishing;
no PyPI token is stored in the repository.

To publish a new version:

1. Update the version in `pyproject.toml`.
2. Commit and push the release changes to `main`.
3. Create a **published GitHub Release** for the matching version.

The workflow is [`.github/workflows/publish.yml`](.github/workflows/publish.yml)
and uses the `pypi` GitHub environment for `tmolavi/answerpath-geo`. The
PyPI-side publisher must remain mapped to Owner `tmolavi`, Repository
`answerpath-geo`, Workflow `publish.yml`, Environment `pypi`.

Do not put a PyPI API token in GitHub secrets or commit it to this repository.

## Quick start

Create a prompt map for a service or keyword:

```bash
answerpath "طراحی سایت فروشگاهی"
```

The command writes `answerpath-output/questions.json` and `questions.csv`.

Analyze owned conversation data and add generated discovery prompts:

```bash
answerpath "مشاوره سئو پزشکی" \\
  --input ~/Downloads/chatgpt-export.zip \\
  --input ./support-chat.json \\
  --out ./research/seo-medical
```

Keep only questions actually found in your supplied data:

```bash
answerpath "سرویس حسابداری" --input ./logs --no-generated
```

## Supported inputs

AnswerPath reads local JSON, JSONL, CSV, directories and ZIP archives. It recognizes common `role=user|human|customer` fields and nested ChatGPT/Claude export structures. It is compatible in principle with exports produced by tools such as [openai_export_parser](https://github.com/temnoon/openai_export_parser), [llm-export-analytics](https://github.com/noah-chelednik/llm-export-analytics), and the local multi-client history model used by [ContextBridgeAI](https://github.com/T-Gojo/ContextBridgeAi).

It does not log in to ChatGPT, Claude, Google, or any other account, scrape other users, or obtain API keys.

## Outputs

Each normalized question contains:

| Field | Meaning |
|---|---|
| `text` | Question text as extracted or generated |
| `evidence` | `observed`, `generated`, or `observed+generated` |
| `source` | Input file or generation rule |
| `intent` | `learn`, `compare`, `buy`, `solve`, `trust`, or `discover` |
| `stage` | Awareness, consideration or decision |
| `frequency` | Number of similar records merged |
| `cluster` | Stable output cluster identifier |

Frequency is meaningful only for observed records from a defined dataset. Template prompts are clearly labeled and must not be reported as customer demand.

## GEO and AEO method

AnswerPath supports a defensible workflow:

1. **Collect** owned exports, support logs or application traces.
2. **Extract** user turns and preserve their source path.
3. **Normalize** whitespace and common message formats.
4. **Classify** intent and decision stage with inspectable rules.
5. **Deduplicate** near-identical questions while retaining frequency.
6. **Expand** with clearly labeled prompt hypotheses when requested.
7. **Publish answers**: create concise answer-first pages, FAQ sections, comparison tables and structured data based on recurring observed questions.
8. **Measure** those prompts in a separate GEO benchmark; never mix hypotheses with measured demand.

The engine does not claim that a page will rank in Google or be cited by an AI system. Those are outcomes to test with your own content and provider evidence.

## Integrations

- **ChatGPT / Claude exports:** pass the downloaded ZIP or extracted JSON to `--input`.
- **Codex, Antigravity, Cursor and other AI IDEs:** export or copy the local session data first; use a read-only copy as input.
- **FAQ workflows:** feed `questions.json` into [FAQ Extraction Pipeline](https://github.com/emfrg/faq-extraction-pipeline) for richer issue extraction, embeddings and FAQ synthesis.
- **GEO prompt discovery:** compare observed questions with generated candidates from projects such as [auto-geo](https://github.com/shadowresearch/auto-geo), keeping the evidence labels separate.

## 🏆 Evidence & Benchmark Contribution

AnswerPath GEO generated the **Question Discovery & Intent Stratification Layer** used in the official [GEO, SEO & Digital Marketing Agency Iran 2026 Benchmark](https://github.com/tmolavi/geo-scope/tree/main/benchmarks/geo-seo-digital-agency-iran-2026.1):

- **Verified Query Dataset**: [`examples/sample_queries.json`](examples/sample_queries.json)
- **Standalone Offline Demo**: [`examples/public_demo/`](examples/public_demo/README.md)
- **Cross-Repository Evidence Map**: [Ecosystem Evidence Flow](https://github.com/tmolavi/geo-scope/blob/main/docs/EVIDENCE_MAP.md)

* **Prompts Generated & Stratified**: 30 standardized queries.
* **Strict Demand Provenance Separation**:
  * **Observed User Demand ($N=15$)**: Extracted from genuine conversational search logs (`source_type: "observed"`).
  * **Exploration Hypotheses ($N=15$)**: Systematic template variations (`source_type: "generated"`).
* **5 Intent Strata**: `commercial` (general evaluation), `compare` (head-to-head alternatives), `trust` (credibility & contracts), `solve` (technical fixes), and `buy` (procurement & quotes).
* **Provenance Contract Schema**:
  ```json
  {
    "id": "PRM-IR-001",
    "prompt": "بهترین آژانس دیجیتال مارکتینگ و سئو در ایران کدام است؟",
    "intent": "commercial",
    "source_type": "observed",
    "source_reference": "answerpath",
    "cluster": "general_recommendation"
  }
  ```
* **Ecosystem Architecture**: See [Benchmark Ecosystem Map](docs/BENCHMARK_ECOSYSTEM.md) for data flow across AnswerPath, GEO-Scope, SAGE, MAVI, and SiteProbe.

## 🏛️ Ecosystem

AnswerPath GEO operates as the question discovery component of the **Molavi AI Visibility Stack**:

- **Discovery**: [AnswerPath GEO](https://github.com/tmolavi/answerpath-geo)
- **Measurement**: [GEO-Scope](https://github.com/tmolavi/geo-scope)
- **Diagnostics**: [SAGE Audit](https://github.com/tmolavi/sage-audit)
- **Action**: [SiteProbe](https://github.com/tmolavi/siteprobe)
- **Protocol**: [MCP GEO Server](https://github.com/tmolavi/mcp-geo-server)

## 📖 Runnable Python Example

Run the bundled discovery example script:
```bash
python examples/discover_example.py
```
Sample benchmark query payload is available in [`examples/sample_queries.json`](examples/sample_queries.json).

## MCP setup

AnswerPath exposes one MCP tool, `discover_questions`. The stdio transport works with local Codex, Antigravity, Claude Desktop, Cursor, Windsurf and other MCP clients:

```json
{
  "mcpServers": {
    "answerpath": {
      "command": "/absolute/path/to/answerpath-geo/.venv/bin/answerpath",
      "args": ["mcp"]
    }
  }
}
```

Ask the client to call `discover_questions` with `topic`, optional owned `inputs` (`text` and `source`), and `include_generated`. Generated prompts are always labeled separately from observed questions.

For a private Cloud deployment, run the HTTP transport behind HTTPS and an authentication gateway:

```bash
answerpath serve-mcp --host 127.0.0.1 --port 8787
```

The JSON-RPC endpoint is `POST /mcp`. The application deliberately does not implement authentication itself: put it behind your gateway, rate limits and tenant isolation before exposing it publicly. A public URL or a successful protocol handshake does not prove that provider data is available.

## Privacy and data boundaries

Processing is local and deterministic. AnswerPath does not transmit input files. Do not place private exports in a public repository or commit generated files containing message content. Remove or hash identifiers before sharing results. Only analyze data for which you have authorization.

## Development & Testing

```bash
pip install -e .
pytest tests/ -v
```

## 💬 Community & External Collaboration

We welcome contributions to query mining, clustering algorithms, and demand stratification:

- **Discussions**: [GitHub Discussions](https://github.com/tmolavi/answerpath-geo/discussions)
- **First Contribution Guide**: [`docs/FIRST_CONTRIBUTION.md`](docs/FIRST_CONTRIBUTION.md)
- **Research Collaboration**: [`docs/RESEARCH_COLLABORATION.md`](docs/RESEARCH_COLLABORATION.md)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/tmolavi/answerpath-geo/issues)
- **Contribution Standards**: [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md)

## 👤 Author & License

Developed by **Taghi Molavi** — [molavi.pro](https://molavi.pro)  
MIT. See [LICENSE](LICENSE).
