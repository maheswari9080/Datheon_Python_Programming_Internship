#!/usr/bin/env python3
"""Rule-Based Interactive Terminal FAQ Assistant.

Datheon Python Internship - Task 04.
Executable via:
    python task4_chatbot/chatbot.py
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from task4_chatbot.faq_loader import DEFAULT_FAQ_PATH, FAQLoader
from task4_chatbot.intent_classifier import RuleBasedMatcher

BANNER = r"""
================================================================================
                    INTERACTIVE TERMINAL FAQ ASSISTANT                          
                    Datheon Python Internship Project 04                        
================================================================================
"""


def run_interactive_session(data_path: Optional[Path] = None) -> None:
    """Run interactive terminal chatbot loop."""
    loader = FAQLoader(data_path or DEFAULT_FAQ_PATH)
    matcher = RuleBasedMatcher(loader)

    print(BANNER)
    print(f"Status: Knowledge Base {loader.status}")
    print("Welcome! Type your questions below. Type 'help' for topics or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated by user. Goodbye!")
            break

        result = matcher.evaluate(user_input)

        print(f"\nAssistant:\n{result.response}\n" + "-" * 60)

        if result.intent == "EXIT":
            break


def main() -> None:
    """CLI Entry point supporting single query mode or full interactive loop."""
    parser = argparse.ArgumentParser(
        description="Rule-Based FAQ Chatbot (Datheon Python Internship Task 4)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Run a single query non-interactively and exit (useful for automated testing).",
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default=None,
        help="Custom path to sample_faq.json dataset.",
    )
    args = parser.parse_args()

    custom_path = Path(args.data_file) if args.data_file else None

    if args.query:
        loader = FAQLoader(custom_path or DEFAULT_FAQ_PATH)
        matcher = RuleBasedMatcher(loader)
        res = matcher.evaluate(args.query)
        print(res.response)
        return

    run_interactive_session(custom_path)


if __name__ == "__main__":
    main()
