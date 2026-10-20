#!/usr/bin/env python3
"""Hangman - Interactive Console Word Guessing Game.

Datheon Python Internship - Task 01.
Executable via:
    python task1_hangman/hangman.py
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Support running directly or as a module
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from task1_hangman.game_engine import HangmanGame, select_secret_word
from task1_hangman.graphics import (
    DEFEAT_BANNER,
    GAME_BANNER,
    VICTORY_BANNER,
    render_board,
)
from task1_hangman.word_loader import DEFAULT_DATA_PATH, load_candidate_words


def play_session(
    secret_word: Optional[str] = None,
    words_pool: Optional[List[str]] = None,
    data_path: Optional[Path] = None,
) -> bool:
    """Run an interactive console game of Hangman until win, loss, or exit.

    Args:
        secret_word: Specific secret word override (useful for testing).
        words_pool: Candidate words list override.
        data_path: Custom path to words.txt.

    Returns:
        True if player won, False if lost.
    """
    if secret_word is None:
        if words_pool is None:
            words_pool = load_candidate_words(data_path or DEFAULT_DATA_PATH)
        secret_word = select_secret_word(words_pool)

    game = HangmanGame(secret_word=secret_word, max_mistakes=6)

    print(GAME_BANNER)
    print(f"I have selected a secret word of {len(secret_word)} letters.")
    print("You are permitted up to 6 incorrect guesses before the gallows is complete.")
    print("Enter a single letter at each prompt. Type 'quit' or press Ctrl+C to exit.\n")

    while not game.is_over:
        # Render the current state of the gallows and word
        print(
            render_board(
                mistakes=game.incorrect_count,
                max_mistakes=game.max_mistakes,
                masked_word=game.get_masked_word(),
                guessed_letters=game.guessed_letters,
            )
        )

        try:
            raw_input = input(">> Enter your guess: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nGame interrupted by user. Exiting gracefully. Goodbye!")
            sys.exit(0)

        # Allow user to quit explicitly
        if raw_input.strip().lower() in ("quit", "exit"):
            print(f"\nYou decided to quit. The secret word was: {game.secret_word}")
            return False

        result, message = game.process_guess(raw_input)
        print(f"\n{message}\n" + "-" * 50)

    # Final Board rendering
    print(
        render_board(
            mistakes=game.incorrect_count,
            max_mistakes=game.max_mistakes,
            masked_word=game.get_masked_word(),
            guessed_letters=game.guessed_letters,
        )
    )

    if game.is_won:
        print(VICTORY_BANNER)
        print(f"  The secret word was indeed: {game.secret_word}!\n")
        return True
    else:
        print(DEFEAT_BANNER)
        print(f"  The secret word was: {game.secret_word}\n")
        return False


def main() -> None:
    """Entry point with CLI argument parsing and replay loop."""
    parser = argparse.ArgumentParser(
        description="Hangman - Word Guessing Challenge (Datheon Python Internship Task 1)",
    )
    parser.add_argument(
        "--word",
        type=str,
        default=None,
        help="Specify an explicit secret word for non-random / automated play.",
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default=None,
        help="Custom path to words dataset file.",
    )
    args = parser.parse_args()

    custom_data_path = Path(args.data_file) if args.data_file else None

    # Load candidate words once for the session
    words = load_candidate_words(custom_data_path)

    while True:
        play_session(secret_word=args.word, words_pool=words)

        # If a single word was forced via CLI flag, do not loop
        if args.word is not None:
            break

        try:
            replay = input("Would you like to play another round? (y/n): ").strip().lower()
            if replay not in ("y", "yes"):
                print("\nThank you for playing Hangman! Have a great day!\n")
                break
            print("\n" + "=" * 60 + "\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
