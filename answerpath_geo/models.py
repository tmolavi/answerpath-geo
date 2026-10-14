"""Data models and schemas for AnswerPath GEO."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Question:
    """Represents a discovered or generated user query.
    Maintains 100% backward compatibility with legacy fields while
    conforming to the Molavi AI Visibility Stack & GEO-Scope benchmark schema.
    """
    text: str
    source: str = "answerpath:synthetic"
    evidence: str = "generated"  # observed | generated | observed+generated
    intent: str = "learn"        # learn | compare | buy | solve | trust | audit
    stage: str = "awareness"     # awareness | consideration | decision | retention
    frequency: int = 1
    cluster: int = -1

    # Rich benchmark & multimodal fields
    id: str = ""
    prompt: str = ""
    modality: str = "text"       # text | voice | multimodal_image
    persona: str = "general_user"
    source_type: str = "generated"  # observed | generated
    source_reference: str = "answerpath"
    cluster_label: str = "general_query"
    image_context: str = ""      # Context description for multimodal image queries
    voice_markers: str = ""      # Spoken dialogue markers for voice queries
    language: str = "auto"
    target_entities: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.prompt:
            self.prompt = self.text
        if not self.text:
            self.text = self.prompt
        if not self.source_type:
            self.source_type = "observed" if self.evidence.startswith("observed") else "generated"
        if not self.source_reference:
            self.source_reference = self.source

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Ensure both text and prompt are synced
        d["text"] = self.text
        d["prompt"] = self.prompt
        return d

@dataclass
class WebsiteContext:
    """Extracted semantic context from a target website or domain."""
    url: str
    domain: str
    brand: str
    title: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    language: str = "fa"
    offerings: list[str] = field(default_factory=list)
