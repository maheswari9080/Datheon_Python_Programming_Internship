"""Rule-based intent classifier and token scoring engine for Task 4 Chatbot."""

import re
import string
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from task4_chatbot.faq_loader import FAQLoader


def normalize_text(text: str) -> str:
    """Normalize input: lowercase, trim, and collapse punctuation/whitespace."""
    lowered = text.lower().strip()
    # Replace punctuation with spaces
    table = str.maketrans(string.punctuation, " " * len(string.punctuation))
    cleaned = lowered.translate(table)
    # Collapse multiple whitespaces
    return " ".join(cleaned.split())


def get_tokens(text: str) -> Set[str]:
    """Tokenize normalized text into a set of words, excluding common stop words."""
    stop_words = {"a", "an", "the", "is", "are", "do", "does", "i", "my", "your", "to", "what", "when", "how"}
    words = normalize_text(text).split()
    return {w for w in words if w not in stop_words and len(w) > 1}


@dataclass
class MatchResult:
    """Holds matching evaluation outcome."""
    intent: str
    response: str
    confidence: float
    matched_question: Optional[str] = None


class RuleBasedMatcher:
    """Intelligent rule-based evaluator with token scoring and specificity priority."""

    def __init__(self, loader: Optional[FAQLoader] = None) -> None:
        self.loader = loader or FAQLoader()
        self.greetings_set = set(self.loader.greetings)
        # Add basic default greetings
        self.greetings_set.update({"hello", "hi", "hey", "greetings", "good morning", "good afternoon"})

        # Regex patterns for high-priority terminal commands
        self.exit_pattern = re.compile(r"^(bye|goodbye|exit|quit|close|cya|see you)$", re.IGNORECASE)
        self.help_pattern = re.compile(r"^(help|\?|commands|what can you do|options)$", re.IGNORECASE)

    def evaluate(self, raw_input: str) -> MatchResult:
        """Evaluate raw user input and determine the best response."""
        cleaned = raw_input.strip()
        if not cleaned:
            return MatchResult(
                intent="EMPTY",
                response="It looks like you entered an empty message. Please ask me a question or type 'help'.",
                confidence=1.0,
            )

        norm_input = normalize_text(cleaned)

        # 1. Check Exit commands
        if self.exit_pattern.match(cleaned) or cleaned.lower() in ("exit", "quit", "bye"):
            return MatchResult(
                intent="EXIT",
                response="Goodbye! Best wishes with your Python internship journey!",
                confidence=1.0,
            )

        # 2. Check Help commands
        if self.help_pattern.match(cleaned) or cleaned.lower() == "help":
            topics_list = "\n".join(f"  * {item['question']}" for item in self.loader.faq_items)
            return MatchResult(
                intent="HELP",
                response=(
                    "Here are the topics I can help you with based on our verified FAQ knowledge base:\n"
                    f"{topics_list}\n\n"
                    "Commands:\n"
                    "  * 'help'  - View this guide\n"
                    "  * 'exit'  - Conclude the chat session"
                ),
                confidence=1.0,
            )

        # 3. Check Greeting intent
        # Direct greeting match or starting with a greeting
        input_words = norm_input.split()
        if any(norm_input == g or norm_input.startswith(f"{g} ") for g in self.greetings_set):
            # Check if there is also an FAQ query attached after the greeting
            # e.g., "Hello, what are your hours?"
            remaining = re.sub(r"^(hello|hi|hey|good morning|good afternoon)\s*", "", norm_input).strip()
            if remaining:
                sub_res = self._match_faqs(remaining)
                if sub_res.confidence >= 0.5:
                    return MatchResult(
                        intent=sub_res.intent,
                        response=f"Hello! {sub_res.response}",
                        confidence=sub_res.confidence,
                        matched_question=sub_res.matched_question,
                    )
            return MatchResult(
                intent="GREETING",
                response="Hello! I am your Datheon Internship Assistant. How may I assist you today? (Type 'help' to see sample questions)",
                confidence=0.95,
            )

        # 4. Check Unsupported / Fabricated Categories (e.g. Pricing, fees, sales)
        # Requirement: "Never fabricate business hours, product features, policies, prices..."
        pricing_terms = {"price", "pricing", "cost", "fee", "fees", "pay", "payment", "subscription"}
        if any(term in input_words for term in pricing_terms):
            return MatchResult(
                intent="UNAVAILABLE_PRICING",
                response=(
                    "Pricing and commercial billing information is unavailable in our dataset. "
                    "The Datheon Python Internship is an educational program. Please contact program "
                    "support for official administrative questions."
                ),
                confidence=0.9,
            )

        # 5. Search FAQs with token scoring & priority
        faq_result = self._match_faqs(norm_input)
        if faq_result.confidence >= 0.4:
            return faq_result

        # 6. Fallback: Unknown query
        suggestions = "\n".join(f"  * {item['question']}" for item in self.loader.faq_items[:3])
        return MatchResult(
            intent="UNKNOWN",
            response=(
                "I am sorry, but I do not have verified information in my dataset for that question.\n"
                "Here are some questions I CAN answer:\n"
                f"{suggestions}\n\n"
                "Or type 'help' for full instructions."
            ),
            confidence=0.0,
        )

    def _match_faqs(self, normalized_query: str) -> MatchResult:
        """Find best matching FAQ item using exact match and token overlap scoring."""
        query_tokens = get_tokens(normalized_query)
        best_score = 0.0
        best_item: Optional[Dict[str, str]] = None

        for item in self.loader.faq_items:
            q_text = item["question"]
            norm_q = normalize_text(q_text)

            # Exact match gives perfect 1.0 score
            if normalized_query == norm_q:
                return MatchResult(
                    intent="FAQ_MATCH",
                    response=item["answer"],
                    confidence=1.0,
                    matched_question=q_text,
                )

            # Substring match (e.g. "hours of operation" in query)
            if norm_q in normalized_query or normalized_query in norm_q:
                score = 0.85
                if score > best_score:
                    best_score = score
                    best_item = item

            # Token overlap scoring (Jaccard similarity)
            q_tokens = get_tokens(q_text)
            if query_tokens and q_tokens:
                intersection = query_tokens.intersection(q_tokens)
                union = query_tokens.union(q_tokens)
                jaccard = len(intersection) / len(union) if union else 0.0

                # Specific question boost: if critical keywords like 'certificate' or 'submit' match
                keyword_boost = 0.0
                if ("certificate" in query_tokens and "certificate" in q_tokens) or \
                   ("submit" in query_tokens and "submit" in q_tokens) or \
                   ("hours" in query_tokens and "hours" in q_tokens):
                    keyword_boost = 0.35

                combined_score = jaccard + keyword_boost
                if combined_score > best_score:
                    best_score = combined_score
                    best_item = item

        if best_item is not None and best_score >= 0.4:
            return MatchResult(
                intent="FAQ_MATCH",
                response=best_item["answer"],
                confidence=round(min(1.0, best_score), 2),
                matched_question=best_item["question"],
            )

        return MatchResult(intent="NO_MATCH", response="", confidence=0.0)
