# AnswerPath GEO Public Demo

`[STANDALONE_DEMO_FIXTURE]` — **Offline Question Discovery & Provenance Formatting**

This demo shows how AnswerPath GEO systematically discovers search and conversational questions, categorizes intent strata, and formats structured prompts with cryptographic provenance for ingestion by GEO-Scope benchmarks.

---

## Files

| File | Description |
|------|-------------|
| `sample_input.json` | Configuration containing target topic, domain, and entity seeds |
| `sample_output.json` | Structured output prompts with full intent and evidence provenance |
| `run_demo.py` | Executable script generating the structured benchmark prompts |

---

## 🚀 How to Run (Under 10 Seconds)

```bash
python examples/public_demo/run_demo.py
```

### Expected Output
```text
======================================================================
AnswerPath GEO: Public Question Discovery & Provenance Demo
======================================================================
• Topic               : خدمات سئو و دیجیتال مارکتینگ در ایران
• Evaluated Entities  : Web24, Novin, Dimarketing, Inten
• Execution Mode      : standalone_demo_fixture (offline)
----------------------------------------------------------------------
✓ Generated 4 structured prompt records.
✓ Output saved to: sample_output.json
======================================================================
Ready for GEO-Scope benchmark execution.
======================================================================
```
