# AnswerPath GEO — Discover the Questions People Ask AI Before They Find Your Business

[![PyPI version](https://img.shields.io/pypi/v/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![Python versions](https://img.shields.io/pypi/pyversions/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/taqimolavi/answerpath-geo)

**AnswerPath GEO** is a privacy-first, open-source **AI Keyword & Question Mining Engine for SEO, GEO (Generative Engine Optimization), and AEO (Answer Engine Optimization)**. Give it a business, service, website URL or topic, and it mines the authentic conversational questions, voice dictations, and multimodal (image/screenshot) queries that real humans ask AI engines (ChatGPT, Perplexity, Claude, Gemini, SearchGPT) before choosing a provider.

It maintains a strict epistemic boundary: separating **observed questions** extracted from owned exports and application logs from **generated research prompts**.

**Languages:** [فارسی](README.fa.md) · [Türkçe](README.tr.md) · [Azərbaycan dili](README.az.md) · [العربية](README.ar.md)

**Try it:** [PyPI package](https://pypi.org/project/answerpath-geo/) · [Hugging Face demo](https://huggingface.co/spaces/taqimolavi/answerpath-geo)

---

## شروع خیلی ساده (برای تیم)

AnswerPath کی‌ورد ریسرچ عصر هوش مصنوعی است: به جای عبارات کوتاه و کلیدواژه‌ای موتورهای جستجوی سنتی، پرسش‌های واقعی، محاوره‌ای، صوتی (Voice) و تصویری (Multimodal) کاربران را شبیه‌سازی و استخراج می‌کند.

### آیا سرویس خارجی یا کلید API می‌خواهد؟

خیر. برای حالت معمول، فقط Python 3.10 یا جدیدتر لازم است. ابزار کاملاً محلی (Local-first) و بدون وابستگی اجرا می‌شود، به هیچ حساب یا API خارجی متصل نمی‌شود و داده‌های شما را به جایی ارسال نمی‌کند.

### سریع‌ترین استفاده

```bash
pip install answerpath-geo
answerpath "طراحی سایت فروشگاهی"
```

یا مستقیماً با دادن آدرس وب‌سایت:

```bash
answerpath https://novin.com
```

سه فایل در پوشه‌ی `answerpath-output/` ساخته می‌شود:
1. `questions.json`: تمام فیلدهای غنی سوالات به همراه نوع رسانه (متن، صوت، تصویر)، پرسونای کاربر و دسته‌بندی قصد خرید.
2. `questions.csv`: برای باز کردن آسان در Excel یا Google Sheets.
3. `benchmark_prompts.json`: فرمت استاندارد برای بنچمارک‌های ارزیابی GEO-Scope.

### شبیه‌سازی انواع روش‌های پرسش از هوش مصنوعی (Modality)

کاربران امروزی به ۳ شکل با مدل‌های زبانی تعامل دارند که همگی توسط AnswerPath پشتیبانی می‌شوند:
- **متنی محاوره‌ای (Conversational Text)**: پرسش‌های چندجمله‌ای شامل سناریوی واقعی، دغدغه و مقایسه.
- **صوتی و ویس (Voice Dictation)**: لحن محاوره‌ای گفتاری با اصطلاحات رایج صوتی («سلام چت‌جی‌پی‌تی...»، «ببین من الان...»).
- **چندحالته و تصویری (Multimodal / Vision)**: آپلود اسکرین‌شات از سایت رقیب، پیش‌فاکتور، نمودار افت سرچ‌کنسول یا جدول تعرفه‌ها به همراه متن ارزیابی تصویر.

```bash
# فقط سوالات صوتی و ویس
answerpath "خدمات سئو" --modality voice

# فقط سوالات چندحالته تصویری با زمینه عکس
answerpath "خدمات ابری" --modality image

# تعیین زبان خروجی (fa, en, tr, ar)
answerpath "طراحی سایت" --lang fa --count 25
```

---

[Installation](#installation) · [Quick start](#quick-start) · [Inputs](#supported-inputs) · [Outputs](#outputs) · [GEO/AEO method](#geo-and-aeo-method) · [Privacy](#privacy-and-data-boundaries) · [Integrations](#integrations)

**MCP clients:** [Codex, Antigravity, Claude, Cursor and Cloud setup](#mcp-setup)

## Why AnswerPath GEO?

Traditional keyword research tools (Ahrefs, Semrush) report short keyword fragments entered into search bars (`seo agency tehran`). AI search engines (ChatGPT Search, Perplexity Sonar, Gemini Grounding, Claude) receive complex, conversational prompts:
- *“I run an online boutique in Tehran. Should I hire an in-house SEO or contract an agency? What's a fair monthly retainer in 2026?”*
- *“Hey ChatGPT, an agency quoted me \$2,000/mo claiming guaranteed #1 rankings in two months. Is that a scam?”*
- *“[Attached screenshot of Search Console drop]: What technical issues caused this organic traffic loss and which agency specializes in penalty recovery?”*

AnswerPath bridges this gap:
- **Zero Hallucinated Keywords**: Models authentic user queries instead of robotic translations.
- **Website URL Analysis**: Ingests domain metadata to tailor questions to your brand and competitors.
- **Multi-Modality**: Simulates typed queries, voice speech transcriptions, and vision/image uploads.
- **Persona & Funnel Stratification**: Classifies by user persona (`business_owner`, `technical_buyer`, `skeptical_customer`, `marketing_lead`) and acquisition stage (`awareness`, `consideration`, `decision`, `retention`).
- **GEO-Scope Benchmark Compatible**: Directly exports prompt banks conforming to the Molavi AI Visibility Stack.

## Installation

Requires Python 3.10+.

```bash
pip install answerpath-geo
```

Or for development:

```bash
git clone https://github.com/tmolavi/answerpath-geo.git
cd answerpath-geo
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick start

### 1. By Topic / Keyword
```bash
answerpath "طراحی سایت فروشگاهی"
```

### 2. By Website URL (Auto-Extracts Brand & Competitive Context)
```bash
answerpath https://example.com --count 30
```

### 3. Mine Real Chat Exports (Privacy-First Observed Queries)
```bash
answerpath "خدمات سئو" \
  --input ~/Downloads/chatgpt-export.zip \
  --input ./support-chat.json \
  --out ./research/seo-output
```

### 4. Keep Only Observed Real Queries (No Synthetic Prompts)
```bash
answerpath "حسابداری آنلاین" --input ./logs/chat.json --no-generated
```

## Supported Inputs

AnswerPath reads local JSON, JSONL, CSV, directories and ZIP archives containing owned conversation logs. It recognizes `role=user|human|customer` fields and nested export structures from ChatGPT, Claude, and custom customer chat exports.

It does **not** scrape provider accounts, log into user portals, or send conversation data over external networks.

## Outputs & Schema

Each query record contains:

| Field | Description | Example |
|---|---|---|
| `id` | Unique prompt identifier | `AP-PRM-001` |
| `prompt` (or `text`) | Natural human question asked to AI | *"من یک فروشگاه اینترنتی نوپا دارم..."* |
| `modality` | Input modality | `text`, `voice`, `multimodal_image` |
| `persona` | Inferred user persona | `business_owner`, `technical_buyer`, `skeptical_customer` |
| `intent` | Core intent category | `learn`, `compare`, `buy`, `solve`, `trust`, `audit` |
| `stage` | Customer acquisition stage | `awareness`, `consideration`, `decision`, `retention` |
| `source_type` | Provenance classification | `observed` (from logs) or `generated` (simulated) |
| `source_reference` | Origin tracking | `answerpath:text`, `answerpath:voice`, `support.json` |
| `cluster_label` | Topic cluster name | `hiring_vs_outsourcing`, `pricing_transparency` |
| `image_context` | Context for multimodal queries | *"اسکرین‌شات از معماری رابط کاربری رقیب"* |
| `voice_markers` | Spoken preamble markers | *"سلام چت‌جی‌پی‌تی، ببین من..."* |
| `frequency` | Occurrence count in observed logs | `1`, `42` |

## 🏆 Evidence & Benchmark Contribution

AnswerPath GEO generated the **Question Discovery & Intent Stratification Layer** used in the official [GEO, SEO & Digital Marketing Agency Iran 2026 Benchmark](https://github.com/tmolavi/geo-scope/tree/main/benchmark/releases/geo-seo-digital-agency-iran-2026.1):

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

AnswerPath GEO is part of the **Molavi AI Visibility Stack**:

- **Discovery**: [AnswerPath GEO](https://github.com/tmolavi/answerpath-geo) — Mines conversational, voice, and multimodal questions.
- **Measurement**: [GEO-Scope](https://github.com/tmolavi/geo-scope) — Multi-model benchmark execution across Gemini, OpenAI, Claude, Perplexity.
- **Diagnostics**: [SAGE Audit](https://github.com/tmolavi/sage-audit) — Pre-retrieval technical & semantic citation diagnostics.
- **Action**: [SiteProbe](https://github.com/tmolavi/siteprobe) — Autonomous code & structured data remediation.
- **Protocol**: [MCP GEO Server](https://github.com/tmolavi/mcp-geo-server) — Standard Model Context Protocol interface.

## MCP Setup

AnswerPath includes a zero-dependency MCP server (`discover_questions` tool) compatible with Codex, Antigravity, Claude Desktop, Cursor, and Windsurf:

```json
{
  "mcpServers": {
    "answerpath": {
      "command": "python3",
      "args": ["-m", "answerpath_geo", "mcp"]
    }
  }
}
```

Or serve via HTTP:

```bash
answerpath serve-mcp --host 127.0.0.1 --port 8787
```

## Privacy & Data Boundaries

All processing is deterministic and strictly local. AnswerPath never transmits input files or sensitive customer chats to third parties.

## Development & Testing

```bash
pip install -e .
pytest tests/ -v
```

## 👤 Author & License

Developed by **Taghi Molavi** — [molavi.pro](https://molavi.pro)  
License: [MIT](LICENSE).
