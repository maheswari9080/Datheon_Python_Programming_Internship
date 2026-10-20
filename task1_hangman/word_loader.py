"""Word loading and dataset sanitation module for Hangman."""

from pathlib import Path
from typing import List, Optional

# Verified offline fallback word list adhering to game standards (length 4-10)
FALLBACK_WORDS: List[str] = [
    "PYTHON",
    "DEVELOPER",
    "PROGRAMMING",
    "ALGORITHM",
    "VARIABLE",
    "FUNCTION",
    "DATABASE",
    "INTERFACE",
    "ENGINEERING",
    "FRAMEWORK",
    "REPOSITORY",
    "AUTOMATION",
]

DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "data" / "words.txt"


def load_candidate_words(
    filepath: Optional[Path] = None,
    min_length: int = 4,
    max_length: int = 10,
) -> List[str]:
    """Load, filter, and sanitize candidate words from disk or return fallback.

    Args:
        filepath: Optional Path to words file. Defaults to data/words.txt.
        min_length: Minimum word length to filter suitable Hangman candidates.
        max_length: Maximum word length to prevent excessively long words.

    Returns:
        List of uppercase alphabetic words.
    """
    target_path = filepath if filepath is not None else DEFAULT_DATA_PATH
    candidates: List[str] = []

    if target_path.exists() and target_path.is_file():
        try:
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip().upper()
                    # Filter: must be strictly alphabetic and within valid length
                    if word.isalpha() and min_length <= len(word) <= max_length:
                        candidates.append(word)
        except Exception:
            candidates = []

    # If the file had no valid candidate words or failed to load, use fallback
    if not candidates:
        return list(FALLBACK_WORDS)

    # Deduplicate while preserving order
    return list(dict.fromkeys(candidates))
