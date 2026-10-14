#!/usr/bin/env python3
"""
Executable example showing how to use AnswerPath GEO Python API
to discover user questions, classify intent, and format provenance records.
"""

import json
import sys
from pathlib import Path

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from answerpath_geo import mine

def main():
    topic = "خدمات سئو و بهینه‌سازی سایت"
    print(f"=== Discovering questions for topic: '{topic}' ===")
    
    # Mine questions across conversational text, voice, and multimodal vision prompts
    results = mine(topic=topic, include_generated=True, benchmark_format=True)
    
    print(f"Total discovered prompts: {len(results)}")
    print("\nSample Output Record (GEO-Scope Benchmark Compatible):")
    if results:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
        
    print("\n✓ Discovery complete. Records ready for GEO-Scope benchmark ingestion.")

if __name__ == "__main__":
    main()
