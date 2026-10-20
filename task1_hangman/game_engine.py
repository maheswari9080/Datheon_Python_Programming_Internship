"""Pure game logic and state management for Hangman."""

import random
from enum import Enum, auto
from typing import List, Optional, Set, Tuple


class GuessResult(Enum):
    """Result of processing a player's letter guess."""
    CORRECT = auto()
    INCORRECT = auto()
    ALREADY_GUESSED = auto()
    INVALID = auto()
    GAME_OVER = auto()


def select_secret_word(words: List[str], rng: Optional[random.Random] = None) -> str:
    """Select a secret word using random.choice().

    Args:
        words: List of candidate words.
        rng: Optional Random instance for deterministic testing.

    Returns:
        Uppercase secret word string.
    """
    if not words:
        raise ValueError("Candidate words list cannot be empty.")
    chooser = rng if rng is not None else random
    return chooser.choice(words).upper()


def validate_raw_input(raw_input: str) -> Tuple[bool, str]:
    """Validate and normalize raw console input.

    Rules:
    - Must not be empty or solely whitespace.
    - Must be exactly one character.
    - Must be an alphabetic letter (A-Z).

    Returns:
        Tuple of (is_valid: bool, letter_or_message: str)
    """
    cleaned = raw_input.strip()
    if not cleaned:
        return False, "Input cannot be empty. Please enter a letter (A-Z)."
    if len(cleaned) > 1:
        return False, f"Please enter a single letter at a time, not '{cleaned}'."
    if not cleaned.isalpha():
        return False, f"'{cleaned}' is not a valid letter. Please enter A-Z."
    return True, cleaned.upper()


class HangmanGame:
    """Manages the state and rules of a single Hangman session."""

    def __init__(self, secret_word: str, max_mistakes: int = 6) -> None:
        if not secret_word or not secret_word.isalpha():
            raise ValueError("Secret word must be a non-empty alphabetic string.")
        self.secret_word: str = secret_word.upper()
        self.max_mistakes: int = max_mistakes
        self.guessed_letters: Set[str] = set()
        self.incorrect_count: int = 0

    @property
    def remaining_attempts(self) -> int:
        """Return the number of remaining incorrect guesses permitted."""
        return max(0, self.max_mistakes - self.incorrect_count)

    @property
    def is_won(self) -> bool:
        """Player wins when all unique characters in secret word are guessed."""
        unique_secret = set(self.secret_word)
        return unique_secret.issubset(self.guessed_letters)

    @property
    def is_lost(self) -> bool:
        """Player loses after reaching max_mistakes without guessing the word."""
        return self.incorrect_count >= self.max_mistakes and not self.is_won

    @property
    def is_over(self) -> bool:
        """Return True if the game is concluded (either won or lost)."""
        return self.is_won or self.is_lost

    def get_masked_word(self, separator: str = " ") -> str:
        """Return the masked representation of the word (e.g. '_ A _ _ M A N')."""
        chars = [
            char if char in self.guessed_letters else "_"
            for char in self.secret_word
        ]
        return separator.join(chars)

    def process_guess(self, raw_input: str) -> Tuple[GuessResult, str]:
        """Process a guess, updating game state and tracking mistakes.

        Enforces rules:
        - Duplicate guesses NEVER penalize attempt count.
        - Invalid inputs NEVER penalize attempt count.
        - Only a new incorrect letter increments incorrect_count.

        Returns:
            Tuple of (GuessResult, descriptive_message: str)
        """
        if self.is_over:
            return GuessResult.GAME_OVER, "Game has already concluded."

        is_valid, letter_or_msg = validate_raw_input(raw_input)
        if not is_valid:
            return GuessResult.INVALID, letter_or_msg

        letter = letter_or_msg

        if letter in self.guessed_letters:
            return (
                GuessResult.ALREADY_GUESSED,
                f"You already guessed '{letter}'. No penalty applied.",
            )

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            if self.is_won:
                return (
                    GuessResult.CORRECT,
                    f"Brilliant! '{letter}' is in the word! You solved it!",
                )
            return GuessResult.CORRECT, f"Good guess! '{letter}' is in the word."
        else:
            self.incorrect_count += 1
            if self.is_lost:
                return (
                    GuessResult.INCORRECT,
                    f"Sorry, '{letter}' is not in the word. No attempts remaining!",
                )
            return (
                GuessResult.INCORRECT,
                f"Sorry, '{letter}' is not in the word. ({self.remaining_attempts} attempts left)",
            )
