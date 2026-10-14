"""Content & export extraction engine for AnswerPath GEO.
Safely extracts website metadata and owned local chat logs (JSON, JSONL, CSV, ZIP).
"""
from __future__ import annotations
import csv
import json
import re
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from .models import WebsiteContext

def _clean_text(value: Any) -> str:
    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()
    if isinstance(value, list):
        return _clean_text(" ".join(_clean_text(x.get("text", "") if isinstance(x, dict) else x) for x in value))
    if isinstance(value, dict):
        return _clean_text(value.get("content", value.get("text", value.get("message", ""))))
    return ""

def is_url(target: str) -> bool:
    """Checks whether the target looks like a URL or domain name."""
    target = target.strip()
    if re.match(r"^https?://", target, re.IGNORECASE):
        return True
    if re.match(r"^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$", target):
        return True
    return False

def detect_language(text: str) -> str:
    """Detects predominant language from text (fa, ar, tr, en)."""
    if not text:
        return "en"
    # Check Persian-specific characters (گ، چ، پ، ژ، ک، ی)
    persian_specific = len(re.findall(r"[\u06af\u0686\u067e\u0698\u06a9\u06cc]", text))
    arabic_persian = len(re.findall(r"[\u0600-\u06FF]", text))
    total_letters = len(re.findall(r"\w", text)) or 1

    if arabic_persian / total_letters > 0.15:
        if persian_specific > 0 or "این" in text or "در" in text or "از" in text or "به" in text or "برای" in text:
            return "fa"
        return "ar"
    
    # Check Turkish characters (ğ, ş, ı, ö, ü, ç)
    turkish_chars = len(re.findall(r"[ğŞşıöüçĞŞİÖÜÇ]", text))
    if turkish_chars > 1 or any(w in text.lower().split() for w in ["ve", "bir", "bu", "için"]):
        return "tr"

    return "en"

class _SimpleMetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.keywords = []
        self.og_site_name = ""
        self.headings = []
        self.html_lang = ""
        self._in_title = False
        self._in_heading = False
        self._curr_heading = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}
        if tag == "html" and "lang" in attr_dict:
            self.html_lang = attr_dict["lang"].strip()
        elif tag == "title":
            self._in_title = True
        elif tag in {"h1", "h2", "h3"}:
            self._in_heading = True
            self._curr_heading = ""
        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "").strip()
            if name == "description" or prop == "og:description":
                if not self.description:
                    self.description = content
            elif prop == "og:site_name":
                self.og_site_name = content
            elif name == "keywords":
                self.keywords = [k.strip() for k in content.split(",") if k.strip()]

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in {"h1", "h2", "h3"}:
            self._in_heading = False
            if self._curr_heading:
                clean = _clean_text(self._curr_heading)
                if clean and clean not in self.headings:
                    self.headings.append(clean)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_heading:
            self._curr_heading += data

def extract_website_context(target: str, timeout: int = 4) -> WebsiteContext:
    """Extracts semantic metadata and brand signals from a website URL or domain."""
    target = target.strip()
    if not target.startswith(("http://", "https://")):
        url = "https://" + target
    else:
        url = target

    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc or parsed.path.split("/")[0]
    domain_clean = re.sub(r"^www\.", "", domain)
    brand_guess = domain_clean.split(".")[0].capitalize()

    ctx = WebsiteContext(
        url=url,
        domain=domain_clean,
        brand=brand_guess,
        language="fa" if domain_clean.endswith(".ir") else "en"
    )

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 AnswerPathGEO/0.2.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fa,en-US;q=0.9,en;q=0.8"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()
            raw_bytes = resp.read(150000)  # Read up to 150KB for fast head/body scan
            html = raw_bytes.decode(charset, errors="replace")

            parser = _SimpleMetaParser()
            parser.feed(html)

            ctx.title = _clean_text(parser.title)
            ctx.description = _clean_text(parser.description)
            ctx.keywords = parser.keywords[:8]
            ctx.headings = parser.headings[:10]

            # Refine brand
            if parser.og_site_name:
                ctx.brand = parser.og_site_name.strip()
            elif ctx.title:
                parts = re.split(r"[-–—|•:]", ctx.title)
                if len(parts) > 1:
                    ctx.brand = parts[-1].strip() or parts[0].strip()

            # Determine language
            combined_text = f"{ctx.title} {ctx.description} {' '.join(ctx.headings)}"
            ctx.language = detect_language(combined_text)
            
            # Extract offerings from headings / keywords
            offerings = []
            for h in ctx.headings:
                if len(h) < 60 and not any(skip in h.lower() for skip in ["تماس", "درباره", "contact", "about", "login"]):
                    offerings.append(h)
            ctx.offerings = offerings[:5] or ctx.keywords[:5]

    except Exception:
        # Offline or unreachable fallback: Keep safe heuristic defaults
        pass

    return ctx

def extract_records(path: str | Path) -> list[tuple[str, str]]:
    """Read owned exports/logs; never accesses provider accounts or remote chats.
    Returns list of (text, source) tuples.
    """
    p = Path(path)
    rows: list[tuple[str, str]] = []
    files = []

    if p.suffix.lower() == ".zip":
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.lower().endswith((".json", ".jsonl", ".csv")):
                    rows.extend(_read_bytes(n, z.read(n), str(p)))
        return rows

    if p.is_dir():
        files = [x for x in p.rglob("*") if x.suffix.lower() in {".json", ".jsonl", ".csv"}]
    elif p.exists():
        files = [p]

    for f in files:
        rows.extend(_read_bytes(str(f), f.read_bytes(), str(f)))
    return rows

def _read_bytes(name: str, data: bytes, source: str) -> list[tuple[str, str]]:
    try:
        obj = json.loads(data)
    except Exception:
        try:
            obj = [json.loads(x) for x in data.decode("utf-8", errors="replace").splitlines() if x.strip()]
        except Exception:
            obj = None

    if obj is not None:
        return _walk(obj, source)

    try:
        out = []
        for row in csv.DictReader(data.decode("utf-8", errors="replace").splitlines()):
            if str(row.get("role", row.get("speaker", row.get("author", "")))).lower() in {"user", "human", "customer"}:
                t = _clean_text(row.get("content", row.get("text", row.get("message", row.get("prompt", "")))))
                if t:
                    out.append((t, source))
        return out
    except Exception:
        return []

def _walk(obj: Any, source: str) -> list[tuple[str, str]]:
    out = []
    if isinstance(obj, dict):
        role = str(obj.get("role", obj.get("author", obj.get("speaker", "")))).lower()
        if role in {"user", "human", "customer"}:
            t = _clean_text(obj.get("content", obj.get("text", obj.get("message", obj.get("prompt", "")))))
            if t:
                out.append((t, source))
        for v in obj.values():
            out.extend(_walk(v, source))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_walk(v, source))
    return out
