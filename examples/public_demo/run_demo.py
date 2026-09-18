#!/usr/bin/env python3
"""
AnswerPath GEO Public Demo
[STANDALONE_DEMO_FIXTURE] — Offline Question Discovery & Prompt Provenance Formatting

Demonstrates how AnswerPath discovers search/AI queries, classifies intent,
assigns epistemic evidence provenance (observed vs generated), and structures
prompts for downstream ingestion by GEO-Scope benchmark suites.
"""

import json
from pathlib import Path

DEMO_DIR = Path(__file__).parent

def run():
    input_file = DEMO_DIR / "sample_input.json"
    output_file = DEMO_DIR / "sample_output.json"

    with open(input_file, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    topic = input_data.get("topic")
    entities = input_data.get("seed_entities", [])

    print("=" * 70)
    print("AnswerPath GEO: Public Question Discovery & Provenance Demo")
    print("=" * 70)
    print(f"• Topic               : {topic}")
    print(f"• Evaluated Entities  : {', '.join(entities)}")
    print(f"• Execution Mode      : standalone_demo_fixture (offline)")
    print("-" * 70)

    # Discovered & Structured Prompt Records
    prompts = [
        {
            "prompt_id": "AP-PRM-001",
            "question": "بهترین شرکت سئو در ایران برای سایت فروشگاهی کدام است؟",
            "source_type": "observed",
            "intent_stratum": "commercial",
            "target_entities": entities,
            "provenance": {
                "discovered_by": "answerpath_geo",
                "evidence": "observed",
                "frequency": 142,
                "cluster": "agency_selection"
            }
        },
        {
            "prompt_id": "AP-PRM-002",
            "question": "مقایسه وب۲۴ و نوین در سئو تکنیکال و تعرفه خدمات",
            "source_type": "observed",
            "intent_stratum": "comparative",
            "target_entities": ["Web24", "Novin"],
            "provenance": {
                "discovered_by": "answerpath_geo",
                "evidence": "observed",
                "frequency": 88,
                "cluster": "comparative_evaluation"
            }
        },
        {
            "prompt_id": "AP-PRM-003",
            "question": "کدام آژانس خدمات سئو تضمینی و بهینه‌سازی فنی ارائه می‌دهد؟",
            "source_type": "generated",
            "intent_stratum": "informational",
            "target_entities": entities,
            "provenance": {
                "discovered_by": "answerpath_geo",
                "evidence": "generated",
                "frequency": 45,
                "cluster": "service_capabilities"
            }
        },
        {
            "prompt_id": "AP-PRM-004",
            "question": "هزینه سئو ماهانه در شرکت‌های معتبر بازاریابی دیجیتال چقدر است؟",
            "source_type": "observed",
            "intent_stratum": "transactional",
            "target_entities": entities,
            "provenance": {
                "discovered_by": "answerpath_geo",
                "evidence": "observed",
                "frequency": 210,
                "cluster": "pricing_and_packages"
            }
        }
    ]

    output_payload = {
        "status": "success",
        "demo_version": "2026.1",
        "source": "answerpath_geo",
        "total_prompts": len(prompts),
        "prompts": prompts
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {len(prompts)} structured prompt records.")
    print(f"✓ Output saved to: {output_file.name}")
    print("\nSample Output Record:")
    print(json.dumps(prompts[0], indent=2, ensure_ascii=False))
    print("=" * 70)
    print("Ready for GEO-Scope benchmark execution.")
    print("=" * 70)

if __name__ == "__main__":
    run()
