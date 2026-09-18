#!/usr/bin/env python3
"""
Executable example showing how to use AnswerPath GEO Python API
to discover user questions, classify intent, and format provenance records.
"""

import json
from answerpath_geo.core import extract_records, mine

def main():
    topic = "خدمات سئو و بهینه‌سازی سایت"
    print(f"=== Discovering questions for topic: '{topic}' ===")
    
    # Mine questions with clear separation between observed demand and generated templates
    results = mine(topic=topic, include_generated=True)
    
    print(f"Total discovered prompts: {len(results)}")
    print("\nSample Output Record:")
    if results:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
        
    print("\n✓ Discovery complete. Records ready for GEO-Scope benchmark ingestion.")

if __name__ == "__main__":
    main()
