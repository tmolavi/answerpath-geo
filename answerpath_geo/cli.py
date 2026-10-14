"""Command-line interface for AnswerPath GEO.
Mines conversational, voice, and multimodal questions for GEO/AEO optimization.
"""
from __future__ import annotations
import argparse
import sys
from .core import extract_records, mine, write_outputs
from .extractor import is_url

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if argv and argv[0] == "mcp":
        from .mcp import stdio
        stdio()
        return

    if argv and argv[0] in {"serve-mcp", "mcp-http"}:
        from .mcp import http
        p = argparse.ArgumentParser(prog="answerpath serve-mcp")
        p.add_argument("--host", default="127.0.0.1")
        p.add_argument("--port", type=int, default=8787)
        a = p.parse_args(argv[1:])
        http(a.host, a.port)
        return

    p = argparse.ArgumentParser(
        prog="answerpath",
        description="Mine realistic human conversational, voice, and multimodal questions for SEO, GEO, and AEO"
    )
    p.add_argument(
        "topic",
        nargs="?",
        default="",
        help="Service, business topic, website URL, or keyword"
    )
    p.add_argument(
        "--url",
        default=None,
        help="Target website URL to extract entity signals, offerings, and brand context from"
    )
    p.add_argument(
        "--modality",
        choices=["all", "text", "voice", "image", "multimodal_image"],
        default="all",
        help="Query modality to simulate (all, text, voice, image)"
    )
    p.add_argument(
        "--lang",
        choices=["auto", "fa", "en", "tr", "ar"],
        default="auto",
        help="Language for prompt generation (default: auto)"
    )
    p.add_argument(
        "--count",
        type=int,
        default=30,
        help="Target number of prompts to discover/generate (default: 30)"
    )
    p.add_argument(
        "--input",
        action="append",
        default=[],
        help="Owned JSON/JSONL/CSV export or directory containing real user logs; repeatable"
    )
    p.add_argument(
        "--out",
        default="answerpath-output",
        help="Output directory path (default: answerpath-output)"
    )
    p.add_argument(
        "--no-generated",
        action="store_true",
        help="Only keep observed questions extracted from inputs"
    )
    p.add_argument(
        "--benchmark",
        action="store_true",
        help="Export directly in GEO-Scope benchmark schema format"
    )

    a = p.parse_args(argv)

    if not a.topic and not a.url and not a.input:
        p.print_help()
        sys.exit(1)

    effective_topic = a.topic or a.url or ""
    effective_url = a.url
    if not effective_url and is_url(effective_topic):
        effective_url = effective_topic

    rows = []
    for x in a.input:
        rows.extend(extract_records(x))

    modality_choice = a.modality
    if modality_choice == "image":
        modality_choice = "multimodal_image"

    qs = mine(
        topic=effective_topic,
        inputs=rows,
        include_generated=not a.no_generated,
        url=effective_url,
        modalities=modality_choice,
        lang=a.lang,
        count=a.count,
        benchmark_format=False
    )

    out = write_outputs(qs, a.out, benchmark_format=a.benchmark)

    observed_count = sum(getattr(q, "evidence", "").startswith("observed") for q in qs)
    generated_count = len(qs) - observed_count
    voice_count = sum(getattr(q, "modality", "") == "voice" for q in qs)
    image_count = sum(getattr(q, "modality", "") in {"image", "multimodal_image"} for q in qs)

    print(f"✓ Discovered and structured {len(qs)} queries in '{out}':")
    print(f"  • Observed from data : {observed_count}")
    print(f"  • Generated AI prompts: {generated_count} (text: {generated_count - voice_count - image_count}, voice: {voice_count}, multimodal/vision: {image_count})")
    print(f"  • Artifacts: questions.json, questions.csv, benchmark_prompts.json")

if __name__ == "__main__":
    main()
