"""AnswerPath GEO: User question discovery & prompt mining for SEO, GEO, and AEO."""
from .models import Question, WebsiteContext
from .extractor import extract_records, extract_website_context
from .core import mine, write_outputs, classify, stage

__version__ = "0.2.0"
__all__ = [
    "Question",
    "WebsiteContext",
    "extract_records",
    "extract_website_context",
    "mine",
    "write_outputs",
    "classify",
    "stage",
]
