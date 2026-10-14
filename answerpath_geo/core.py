"""Question mining engine: deterministic, local-first, and explicit about evidence.
Supports authentic conversational search, voice dictation, multimodal/vision queries,
and website/URL extraction for GEO and AEO.
"""
from __future__ import annotations
import csv
import json
import re
from dataclasses import asdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from .models import Question, WebsiteContext
from .extractor import extract_records, extract_website_context, is_url, detect_language
from .generator import (
    classify_intent,
    classify_stage,
    generate_realistic_prompts,
    INTENT_MAPPINGS
)

INTENTS = {
    "learn": ["what", "چیست", "چیه", "چطور", "how", "guide", "راهنما", "آموزش"],
    "compare": ["compare", "مقایسه", "بهتر", "vs", "versus", "فرق", "تفاوت", "کدوم"],
    "buy": ["price", "قیمت", "خرید", "buy", "cost", "پکیج", "هزینه", "تعرفه", "پیش‌فاکتور"],
    "solve": ["مناسب", "حل", "مشکل", "نرم افزار", "service", "خدمت", "حل کردن", "رفع", "خطا", "افت"],
    "trust": ["review", "نظرات", "اعتماد", "قابل اعتماد", "تجربه", "شکایت", "کلاهبرداری"],
    "audit": ["audit", "آنالیز", "بررسی", "ممیزی", "ارزیابی", "kpi"],
}

def _clean_text(value: Any) -> str:
    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()
    if isinstance(value, list):
        return _clean_text(" ".join(_clean_text(x.get("text", "") if isinstance(x, dict) else x) for x in value))
    if isinstance(value, dict):
        return _clean_text(value.get("content", value.get("text", value.get("message", ""))))
    return ""

def classify(text: str) -> str:
    """Classifies user intent from natural query text."""
    return classify_intent(text)

def stage(intent: str) -> str:
    """Maps intent to customer acquisition / decision stage."""
    return classify_stage(intent)

def generated_prompts(topic: str, site: WebsiteContext | None = None, lang: str = "auto") -> list[str]:
    """Backward compatible helper returning realistic generated prompt strings."""
    qs = generate_realistic_prompts(topic, site=site, lang=lang, count=16)
    return [q.text for q in qs]

def mine(
    topic: str,
    inputs: Any = (),
    include_generated: bool = True,
    threshold: float = 0.88,
    url: str | None = None,
    modalities: list[str] | str | None = None,
    lang: str = "auto",
    count: int = 30,
    personas: list[str] | None = None,
    benchmark_format: bool = False,
) -> list[Question] | list[dict[str, Any]]:
    """Mines user questions from observed exports, website context, and AI prompt simulation.
    
    Args:
        topic: Service, business, website URL, or keyword.
        inputs: List of (text, source) tuples or export records.
        include_generated: Whether to add generated AI search queries.
        threshold: SequenceMatcher similarity threshold for deduplication.
        url: Optional target website URL to extract entity signals from.
        modalities: Filter or include modalities ('all', 'text', 'voice', 'multimodal_image').
        lang: Language mode ('auto', 'fa', 'en', 'tr', 'ar').
        count: Target number of questions to mine/generate.
        personas: Optional list of personas to prioritize.
        benchmark_format: If True, returns dicts formatted for GEO-Scope benchmark ingestion.
    """
    site_ctx: WebsiteContext | None = None
    target_topic = topic.strip() if topic else ""

    # Check if topic itself is a URL, or if url parameter was passed
    target_url = url
    if not target_url and is_url(target_topic):
        target_url = target_topic

    if target_url:
        site_ctx = extract_website_context(target_url)
        if not target_topic or is_url(target_topic):
            target_topic = site_ctx.title or site_ctx.brand or target_url

    if lang == "auto":
        lang = detect_language(f"{target_topic} {site_ctx.title if site_ctx else ''}")

    # Parse modality argument
    modality_list: list[str] | None = None
    if isinstance(modalities, str):
        modality_list = [modalities]
    elif isinstance(modalities, (list, tuple, set)):
        modality_list = list(modalities)

    qs: list[Question] = []
    
    # 1. Process observed input queries
    obs_idx = 1
    for item in inputs:
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            raw_text, source = item[0], item[1]
        elif isinstance(item, dict):
            raw_text = item.get("text", item.get("prompt", item.get("content", "")))
            source = item.get("source", "export")
        else:
            raw_text, source = str(item), "export"

        text = _clean_text(raw_text)
        if len(text) < 4 or len(text) > 1000:
            continue

        q_intent = classify(text)
        q_stage = stage(q_intent)
        pid = f"AP-OBS-{obs_idx:03d}"
        obs_idx += 1

        qs.append(Question(
            id=pid,
            text=text,
            prompt=text,
            source=source,
            evidence="observed",
            intent=q_intent,
            stage=q_stage,
            frequency=1,
            modality="text",
            persona="observed_user",
            source_type="observed",
            source_reference=source,
            cluster_label=f"observed_{q_intent}",
            language=detect_language(text),
            target_entities=[site_ctx.brand] if site_ctx and site_ctx.brand else []
        ))

    # 2. Generate authentic AI search prompts (text, voice, multimodal)
    if include_generated:
        gen_qs = generate_realistic_prompts(
            topic=target_topic,
            site=site_ctx,
            lang=lang,
            modalities=modality_list,
            count=count
        )
        if personas:
            gen_qs = [q for q in gen_qs if q.persona in personas] or gen_qs
        qs.extend(gen_qs)

    # 3. Deduplication and clustering
    groups: list[Question] = []
    for q in qs:
        match = None
        for existing in groups:
            # Fuzzy match on normalized text
            sim = SequenceMatcher(None, q.text.lower(), existing.text.lower()).ratio()
            if sim >= threshold:
                match = existing
                break

        if match:
            match.frequency += 1
            if q.source not in match.source:
                match.source += f";{q.source}"
            if match.evidence != q.evidence:
                match.evidence = "observed+generated"
                match.source_type = "observed+generated"
        else:
            groups.append(q)

    # Assign sequential cluster IDs
    for i, q in enumerate(groups):
        q.cluster = i
        if not q.id:
            q.id = f"AP-PRM-{i+1:03d}"

    if benchmark_format:
        return [
            {
                "id": q.id,
                "prompt": q.prompt or q.text,
                "intent": q.intent,
                "modality": q.modality,
                "persona": q.persona,
                "stage": q.stage,
                "source_type": q.source_type,
                "source_reference": q.source_reference,
                "cluster": q.cluster_label or str(q.cluster),
                "frequency": q.frequency,
                "evidence": q.evidence,
                "image_context": q.image_context,
                "voice_markers": q.voice_markers,
                "language": q.language,
                "target_entities": q.target_entities,
            }
            for q in groups
        ]

    return groups

def write_outputs(questions: list[Any], out: str | Path, benchmark_format: bool = False) -> Path:
    """Exports discovered and generated questions to JSON and CSV files."""
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not questions:
        raw_data: list[dict[str, Any]] = []
    elif hasattr(questions[0], "to_dict"):
        raw_data = [q.to_dict() for q in questions]
    elif hasattr(questions[0], "__dataclass_fields__"):
        raw_data = [asdict(q) for q in questions]
    elif isinstance(questions[0], dict):
        raw_data = questions
    else:
        raw_data = [{"text": str(q)} for q in questions]

    # Write questions.json
    (out_dir / "questions.json").write_text(
        json.dumps(raw_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Write questions.csv
    with (out_dir / "questions.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(raw_data[0].keys()) if raw_data else ["text"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(raw_data)

    # Write benchmark_prompts.json for GEO-Scope ingestion
    benchmark_records = [
        {
            "id": r.get("id", f"PRM-{i+1:03d}"),
            "prompt": r.get("prompt") or r.get("text", ""),
            "intent": r.get("intent", "learn"),
            "modality": r.get("modality", "text"),
            "persona": r.get("persona", "general_user"),
            "stage": r.get("stage", "awareness"),
            "source_type": r.get("source_type", "generated"),
            "source_reference": r.get("source_reference", "answerpath"),
            "cluster": r.get("cluster_label", str(r.get("cluster", "general"))),
            "evidence": r.get("evidence", "generated"),
            "image_context": r.get("image_context", ""),
            "voice_markers": r.get("voice_markers", ""),
            "language": r.get("language", "en"),
            "target_entities": r.get("target_entities", []),
        }
        for i, r in enumerate(raw_data)
    ]
    (out_dir / "benchmark_prompts.json").write_text(
        json.dumps(benchmark_records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return out_dir
