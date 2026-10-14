#!/usr/bin/env python3
"""
AnswerPath GEO Public Demo
[STANDALONE_DEMO_FIXTURE] — Offline Question Discovery & Prompt Provenance Formatting

Demonstrates how AnswerPath discovers search/AI queries, classifies intent,
assigns epistemic evidence provenance (observed vs generated), and structures
prompts for downstream ingestion by GEO-Scope benchmark suites.
"""

import json
import sys
from pathlib import Path

# Ensure root package is available
DEMO_DIR = Path(__file__).parent
sys.path.insert(0, str(DEMO_DIR.parents[1]))

from answerpath_geo.core import mine

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

    # Discovered & Structured Prompt Records via AnswerPath GEO
    raw_prompts = mine(
        topic=topic,
        include_generated=True,
        benchmark_format=True,
        count=15
    )

    prompts = []
    for idx, p in enumerate(raw_prompts, start=1):
        prompts.append({
            "prompt_id": p["id"],
            "question": p["prompt"],
            "source_type": p["source_type"],
            "intent_stratum": p["intent"],
            "modality": p.get("modality", "text"),
            "target_entities": entities,
            "provenance": {
                "discovered_by": "answerpath_geo",
                "evidence": p["evidence"],
                "frequency": p["frequency"],
                "cluster": p["cluster"],
                "image_context": p.get("image_context", ""),
                "voice_markers": p.get("voice_markers", ""),
            }
        })

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
    if prompts:
        print(json.dumps(prompts[0], indent=2, ensure_ascii=False))
    print("=" * 70)
    print("Ready for GEO-Scope benchmark execution.")
    print("=" * 70)

if __name__ == "__main__":
    run()
