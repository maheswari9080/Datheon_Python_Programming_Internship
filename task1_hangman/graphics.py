"""ASCII gallows graphics and terminal presentation formatting for Hangman."""

from typing import List, Set

# 7 visual ASCII stages corresponding to mistakes 0 through 6
GALLOWS_STAGES: List[str] = [
    # Stage 0: Clean gallows, 0 mistakes
    r"""
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    # Stage 1: Head, 1 mistake
    r"""
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    # Stage 2: Torso, 2 mistakes
    r"""
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    # Stage 3: Left arm, 3 mistakes
    r"""
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    # Stage 4: Right arm, 4 mistakes
    r"""
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========
    """,
    # Stage 5: Left leg, 5 mistakes
    r"""
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========
    """,
    # Stage 6: Right leg (Final), 6 mistakes - Defeat
    r"""
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========
    """,
]

GAME_BANNER = r"""
============================================================
              HANGMAN - WORD GUESSING CHALLENGE             
             Datheon Python Internship Project 01           
============================================================
"""

VICTORY_BANNER = r"""
  * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                     CONGRATULATIONS!                      
               YOU GUESSED THE SECRET WORD!                
  * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

DEFEAT_BANNER = r"""
  ---------------------------------------------------------
                       GAME OVER!                          
            YOU RAN OUT OF ATTEMPTS ON THE GALLOWS.        
  ---------------------------------------------------------
"""


def get_gallows_art(mistakes: int) -> str:
    """Return the ASCII gallows art corresponding to the mistake count (0 to 6)."""
    clamped = max(0, min(mistakes, len(GALLOWS_STAGES) - 1))
    return GALLOWS_STAGES[clamped].strip("\n")


def format_guessed_letters(guessed_letters: Set[str]) -> str:
    """Return a sorted, formatted string of letters guessed so far."""
    if not guessed_letters:
        return "None"
    return ", ".join(sorted(guessed_letters))


def render_board(
    mistakes: int,
    max_mistakes: int,
    masked_word: str,
    guessed_letters: Set[str],
) -> str:
    """Compose the full visual state of the game board."""
    remaining = max(0, max_mistakes - mistakes)
    gallows = get_gallows_art(mistakes)
    guessed_str = format_guessed_letters(guessed_letters)

    return (
        f"{gallows}\n\n"
        f"  Word:               {masked_word}\n"
        f"  Attempts Remaining: {remaining} of {max_mistakes}\n"
        f"  Guessed Letters:    [{guessed_str}]\n"
    )
