"""Automated unittest suite for Task 1 Hangman."""

import tempfile
import unittest
from pathlib import Path

from task1_hangman.game_engine import (
    GuessResult,
    HangmanGame,
    select_secret_word,
    validate_raw_input,
)
from task1_hangman.graphics import get_gallows_art, render_board
from task1_hangman.word_loader import (
    FALLBACK_WORDS,
    load_candidate_words,
)


class TestWordLoader(unittest.TestCase):
    """Verify word loading, dataset filtering, and fallback behaviors."""

    def test_load_existing_dataset(self) -> None:
        words = load_candidate_words()
        self.assertGreater(len(words), 1000)
        self.assertTrue(all(w.isalpha() and w.isupper() for w in words))

    def test_load_missing_file_returns_fallback(self) -> None:
        missing_path = Path("task1_hangman/data/non_existent_file_9999.txt")
        words = load_candidate_words(missing_path)
        self.assertEqual(words, FALLBACK_WORDS)

    def test_load_malformed_file_filters_invalid_lines(self) -> None:
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            tf.write("hello\n12345\nshort\n#invalid!\nsupercalifragilistic\ngoodword\n")
            tf_path = Path(tf.name)

        try:
            words = load_candidate_words(tf_path, min_length=4, max_length=10)
            self.assertIn("HELLO", words)
            self.assertIn("SHORT", words)
            self.assertIn("GOODWORD", words)
            self.assertNotIn("12345", words)
            self.assertNotIn("#INVALID!", words)
            self.assertNotIn("SUPERCALIFRAGILISTIC", words)
        finally:
            tf_path.unlink(missing_ok=True)


class TestInputValidation(unittest.TestCase):
    """Verify raw input normalization and rejection."""

    def test_valid_lowercase_letter(self) -> None:
        valid, letter = validate_raw_input("a")
        self.assertTrue(valid)
        self.assertEqual(letter, "A")

    def test_valid_whitespace_padded_letter(self) -> None:
        valid, letter = validate_raw_input("   z   ")
        self.assertTrue(valid)
        self.assertEqual(letter, "Z")

    def test_empty_input_rejected(self) -> None:
        valid, msg = validate_raw_input("   ")
        self.assertFalse(valid)
        self.assertIn("empty", msg.lower())

    def test_multi_char_input_rejected(self) -> None:
        valid, msg = validate_raw_input("ab")
        self.assertFalse(valid)
        self.assertIn("single letter", msg.lower())

    def test_non_alpha_rejected(self) -> None:
        valid, msg = validate_raw_input("7")
        self.assertFalse(valid)
        self.assertIn("not a valid letter", msg.lower())


class TestHangmanGameEngine(unittest.TestCase):
    """Verify Hangman game state machine transitions and rules."""

    def setUp(self) -> None:
        self.game = HangmanGame(secret_word="PYTHON", max_mistakes=6)

    def test_initial_state(self) -> None:
        self.assertEqual(self.game.remaining_attempts, 6)
        self.assertEqual(self.game.incorrect_count, 0)
        self.assertFalse(self.game.is_won)
        self.assertFalse(self.game.is_lost)
        self.assertFalse(self.game.is_over)
        self.assertEqual(self.game.get_masked_word(), "_ _ _ _ _ _")

    def test_correct_guess_reveals_position(self) -> None:
        res, _ = self.game.process_guess("P")
        self.assertEqual(res, GuessResult.CORRECT)
        self.assertEqual(self.game.remaining_attempts, 6)
        self.assertEqual(self.game.incorrect_count, 0)
        self.assertEqual(self.game.get_masked_word(), "P _ _ _ _ _")

    def test_incorrect_guess_penalizes_attempt(self) -> None:
        res, _ = self.game.process_guess("Z")
        self.assertEqual(res, GuessResult.INCORRECT)
        self.assertEqual(self.game.remaining_attempts, 5)
        self.assertEqual(self.game.incorrect_count, 1)
        self.assertEqual(self.game.get_masked_word(), "_ _ _ _ _ _")

    def test_duplicate_guess_no_penalty(self) -> None:
        # First incorrect guess: reduces remaining to 5
        self.game.process_guess("Z")
        self.assertEqual(self.game.remaining_attempts, 5)

        # Duplicate guess of same letter: NO penalty
        res, msg = self.game.process_guess("Z")
        self.assertEqual(res, GuessResult.ALREADY_GUESSED)
        self.assertEqual(self.game.remaining_attempts, 5)
        self.assertEqual(self.game.incorrect_count, 1)

    def test_duplicate_correct_guess_no_penalty(self) -> None:
        self.game.process_guess("P")
        res, _ = self.game.process_guess("P")
        self.assertEqual(res, GuessResult.ALREADY_GUESSED)
        self.assertEqual(self.game.remaining_attempts, 6)

    def test_invalid_input_no_penalty(self) -> None:
        res, _ = self.game.process_guess("123")
        self.assertEqual(res, GuessResult.INVALID)
        self.assertEqual(self.game.remaining_attempts, 6)

    def test_victory_condition(self) -> None:
        for char in "PYTHON":
            self.game.process_guess(char)

        self.assertTrue(self.game.is_won)
        self.assertFalse(self.game.is_lost)
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.get_masked_word(), "P Y T H O N")

    def test_defeat_condition_at_six_mistakes(self) -> None:
        wrong_letters = ["A", "B", "C", "D", "E", "F"]
        for letter in wrong_letters:
            self.game.process_guess(letter)

        self.assertFalse(self.game.is_won)
        self.assertTrue(self.game.is_lost)
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.remaining_attempts, 0)
        self.assertEqual(self.game.incorrect_count, 6)


class TestGraphics(unittest.TestCase):
    """Verify ASCII gallows and board rendering."""

    def test_gallows_stages_bound(self) -> None:
        for stage in range(7):
            art = get_gallows_art(stage)
            self.assertTrue(len(art) > 10)
            self.assertIn("===", art)

    def test_render_board_contains_elements(self) -> None:
        board = render_board(
            mistakes=2,
            max_mistakes=6,
            masked_word="P _ _ _ _ _",
            guessed_letters={"P", "X", "Y"},
        )
        self.assertIn("Word:               P _ _ _ _ _", board)
        self.assertIn("Attempts Remaining: 4 of 6", board)
        self.assertIn("P, X, Y", board)


if __name__ == "__main__":
    unittest.main()
