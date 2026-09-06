"""Question mining engine: deterministic, local-first, and explicit about evidence."""
from __future__ import annotations
import csv, json, re, zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from difflib import SequenceMatcher

@dataclass
class Question:
    text: str
    source: str
    evidence: str  # observed | generated
    intent: str
    stage: str
    frequency: int = 1
    cluster: int = -1

INTENTS = {
    "learn": ["what", "چیست", "چیه", "چطور", "how", "guide"],
    "compare": ["compare", "مقایسه", "بهتر", "vs", "versus", "فرق"],
    "buy": ["price", "قیمت", "خرید", "buy", "cost", "پکیج", "هزینه"],
    "solve": ["مناسب", "حل", "مشکل", "نرم افزار", "service", "خدمت", "حل کردن"],
    "trust": ["review", "نظرات", "اعتماد", "قابل اعتماد", "تجربه", "review"],
}

def _text(value) -> str:
    if isinstance(value, str): return re.sub(r"\s+", " ", value).strip()
    if isinstance(value, list): return _text(" ".join(_text(x.get("text", "") if isinstance(x, dict) else x) for x in value))
    if isinstance(value, dict): return _text(value.get("content", value.get("text", "")))
    return ""

def extract_records(path: str | Path) -> list[tuple[str, str]]:
    """Read owned exports/logs; never accesses provider accounts or remote chats."""
    p = Path(path); rows=[]
    files=[]
    if p.suffix.lower()==".zip":
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.lower().endswith((".json", ".jsonl", ".csv")): rows.extend(_read_bytes(n, z.read(n), str(p)))
        return rows
    if p.is_dir(): files=[x for x in p.rglob("*") if x.suffix.lower() in {".json", ".jsonl", ".csv"}]
    else: files=[p]
    for f in files: rows.extend(_read_bytes(str(f), f.read_bytes(), str(f)))
    return rows

def _read_bytes(name, data, source):
    try: obj=json.loads(data)
    except Exception:
        try: obj=[json.loads(x) for x in data.decode().splitlines() if x.strip()]
        except Exception: obj=None
    if obj is not None: return _walk(obj, source)
    try:
        out=[]
        for row in csv.DictReader(data.decode().splitlines()):
            if str(row.get("role", row.get("speaker", ""))).lower() in {"user","human","customer"}: out.append((_text(row.get("content", row.get("text", ""))), source))
        return out
    except Exception: return []

def _walk(obj, source):
    out=[]
    if isinstance(obj, dict):
        role=str(obj.get("role", obj.get("author", obj.get("speaker", "")))).lower()
        if role in {"user","human","customer"}:
            t=_text(obj.get("content", obj.get("text", obj.get("message", ""))))
            if t: out.append((t, source))
        for v in obj.values(): out.extend(_walk(v, source))
    elif isinstance(obj, list):
        for v in obj: out.extend(_walk(v, source))
    return out

def classify(text):
    low=text.lower()
    for intent, words in INTENTS.items():
        if any(w in low for w in words): return intent
    return "discover"

def stage(intent): return {"learn":"awareness","compare":"consideration","trust":"consideration","buy":"decision","solve":"decision"}.get(intent,"awareness")

def generated_prompts(topic):
    return [
      f"What is the best {topic} for a small business?",
      f"How do I choose a reliable {topic} provider?",
      f"What should I compare before buying {topic}?",
      f"How much does {topic} cost and what is included?",
      f"Which {topic} is suitable for my needs?",
      f"What are the common problems with {topic} and how are they solved?",
      f"Are there trustworthy reviews or examples for {topic}?",
      f"Compare the leading {topic} options for quality and price.",
    ]

def mine(topic, inputs=(), include_generated=True, threshold=.88):
    qs=[]
    for text, source in inputs:
        text=_text(text)
        if len(text)<4 or len(text)>1000: continue
        intent=classify(text); qs.append(Question(text, source, "observed", intent, stage(intent)))
    if include_generated:
        for text in generated_prompts(topic):
            intent=classify(text); qs.append(Question(text, "answerpath:template", "generated", intent, stage(intent)))
    groups=[]
    for q in qs:
        match=None
        for existing in groups:
            if SequenceMatcher(None, q.text.lower(), existing.text.lower()).ratio()>=threshold:
                match=existing; break
        if match: match.frequency+=1; match.source += ";"+q.source; match.evidence = "observed+generated" if match.evidence!=q.evidence else match.evidence
        else: groups.append(q)
    for i,q in enumerate(groups): q.cluster=i
    return groups

def write_outputs(questions, out):
    out=Path(out); out.mkdir(parents=True, exist_ok=True)
    data=[asdict(q) for q in questions]
    (out/"questions.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out/"questions.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=data[0].keys() if data else ["text"]); w.writeheader(); w.writerows(data)
    return out
