"""FAQ dataset loader and schema adapter for Task 4 Chatbot."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_FAQ_PATH = Path(__file__).resolve().parent / "data" / "sample_faq.json"

FALLBACK_FAQ_DATA: Dict[str, Any] = {
    "greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
    "faqs": [
        {
            "question": "What are your hours of operation?",
            "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST.",
        },
        {
            "question": "How do I submit my internship project?",
            "answer": "You can submit your public GitHub repository link through your Student Workspace.",
        },
        {
            "question": "When will I receive my certificate?",
            "answer": "Certificates are reviewed and issued within 3-5 business days after your code review.",
        },
    ],
}


class FAQLoader:
    """Safely loads and validates the FAQ schema."""

    def __init__(self, json_path: Optional[Path] = None) -> None:
        self.json_path = json_path or DEFAULT_FAQ_PATH
        self.greetings: List[str] = []
        self.faq_items: List[Dict[str, str]] = []
        self.status: str = "unloaded"
        self._load()

    def _load(self) -> None:
        if self.json_path.exists() and self.json_path.is_file():
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        raw_greetings = data.get("greetings", [])
                        raw_faqs = data.get("faqs", [])

                        if isinstance(raw_greetings, list):
                            self.greetings = [str(g).strip().lower() for g in raw_greetings if g]
                        if isinstance(raw_faqs, list):
                            self.faq_items = [
                                {
                                    "question": str(item.get("question", "")).strip(),
                                    "answer": str(item.get("answer", "")).strip(),
                                }
                                for item in raw_faqs
                                if isinstance(item, dict) and item.get("question") and item.get("answer")
                            ]
                        self.status = f"loaded ({len(self.greetings)} greetings, {len(self.faq_items)} faqs)"
                        return
            except Exception as e:
                self.status = f"error loading json: {e}; using fallback"

        # Fallback engagement
        self.greetings = list(FALLBACK_FAQ_DATA["greetings"])
        self.faq_items = list(FALLBACK_FAQ_DATA["faqs"])
        self.status = "fallback loaded"
