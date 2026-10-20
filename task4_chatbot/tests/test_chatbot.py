"""Automated unittest suite for Task 4 Rule-Based Interactive Chatbot."""

import json
import tempfile
import unittest
from pathlib import Path

from task4_chatbot.faq_loader import FAQLoader
from task4_chatbot.intent_classifier import (
    RuleBasedMatcher,
    normalize_text,
)


class TestTextNormalization(unittest.TestCase):
    """Verify string normalization, punctuation removal, and whitespace collapsing."""

    def test_lowercase_and_strip(self) -> None:
        self.assertEqual(normalize_text("  HELLO WORLD  "), "hello world")

    def test_punctuation_removal(self) -> None:
        self.assertEqual(
            normalize_text("What are your hours?! (Tell me...)"),
            "what are your hours tell me",
        )


class TestFAQLoader(unittest.TestCase):
    """Verify loading from valid files, missing files, and malformed JSON."""

    def test_load_default_dataset(self) -> None:
        loader = FAQLoader()
        self.assertGreater(len(loader.greetings), 0)
        self.assertGreater(len(loader.faq_items), 0)
        self.assertTrue(all("question" in item and "answer" in item for item in loader.faq_items))

    def test_missing_file_activates_fallback(self) -> None:
        loader = FAQLoader(Path("non_existent_faq_9999.json"))
        self.assertIn("fallback", loader.status)
        self.assertGreater(len(loader.faq_items), 0)

    def test_malformed_json_activates_fallback(self) -> None:
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json", encoding="utf-8") as tf:
            tf.write("{ this is completely broken json ::: ")
            tf_path = Path(tf.name)

        try:
            loader = FAQLoader(tf_path)
            self.assertIn("fallback", loader.status)
            self.assertGreater(len(loader.faq_items), 0)
        finally:
            tf_path.unlink(missing_ok=True)


class TestChatbotIntentMatching(unittest.TestCase):
    """Verify intent classifications, dataset fidelity, and fallback behavior."""

    def setUp(self) -> None:
        self.matcher = RuleBasedMatcher()

    def test_greeting_intent(self) -> None:
        res = self.matcher.evaluate("Hello there!")
        self.assertEqual(res.intent, "GREETING")
        self.assertIn("Hello!", res.response)

    def test_exit_intent(self) -> None:
        for cmd in ["bye", "exit", "quit", "goodbye"]:
            res = self.matcher.evaluate(cmd)
            self.assertEqual(res.intent, "EXIT")

    def test_help_intent(self) -> None:
        res = self.matcher.evaluate("help")
        self.assertEqual(res.intent, "HELP")
        self.assertIn("Here are the topics", res.response)

    def test_hours_faq_response_from_dataset(self) -> None:
        res = self.matcher.evaluate("What are your hours of operation?")
        self.assertEqual(res.intent, "FAQ_MATCH")
        self.assertIn("Monday through Friday", res.response)
        self.assertIn("9:00 AM to 6:00 PM IST", res.response)

    def test_submission_faq_response_from_dataset(self) -> None:
        res = self.matcher.evaluate("How do I submit my internship project?")
        self.assertEqual(res.intent, "FAQ_MATCH")
        self.assertIn("Student Workspace", res.response)

    def test_certificate_faq_response_from_dataset(self) -> None:
        res = self.matcher.evaluate("When will I get my certificate?")
        self.assertEqual(res.intent, "FAQ_MATCH")
        self.assertIn("3-5 business days", res.response)

    def test_unsupported_pricing_acknowledged_not_fabricated(self) -> None:
        res = self.matcher.evaluate("How much does this cost?")
        self.assertEqual(res.intent, "UNAVAILABLE_PRICING")
        self.assertIn("unavailable", res.response.lower())

    def test_unknown_question_graceful_fallback(self) -> None:
        res = self.matcher.evaluate("Can you bake a chocolate cake for me?")
        self.assertEqual(res.intent, "UNKNOWN")
        self.assertIn("do not have verified information", res.response)
        self.assertIn("Here are some questions I CAN answer", res.response)

    def test_empty_message_handled(self) -> None:
        res = self.matcher.evaluate("   ")
        self.assertEqual(res.intent, "EMPTY")
        self.assertIn("empty message", res.response)


if __name__ == "__main__":
    unittest.main()
