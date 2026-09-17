# AnswerPath GEO — Discover the Questions People Ask AI Before They Find Your Business

**AnswerPath GEO** is a privacy-first, open-source **SEO, GEO and AEO question mining engine**. Give it a business, service, website topic or keyword and it builds a transparent question map showing what people may ask an AI assistant before choosing a provider.

It separates **observed questions** extracted from exports and application logs from **generated research prompts**. This distinction matters: generated prompts are hypotheses, not evidence of what people actually asked.

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
- **GEO-Scope Benchmark Integration:** AnswerPath GEO serves as the official **Question Source & Intent Discovery Layer** for [GEO-Scope](https://github.com/tmolavi/geo-scope) empirical AI visibility studies (such as the *GEO, SEO & Digital Marketing Agency Iran 2026 Benchmark*). It categorizes demand into explicit search intent strata (`commercial`, `compare`, `trust`, `solve`, `buy`) and strictly preserves provenance tags (`source_type: "observed"` vs `"generated"`), preventing synthetic prompt leakage into measured user demand.

These projects are references and adapters, not vendored code. Their licenses and upstream terms remain applicable.

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

## Development

```bash
.venv/bin/pip install -e '.[dev]'  # if dev extras are added by a downstream fork
python -m pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
