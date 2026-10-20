# Task 01: Hangman Word Guessing Game

Part of the **Datheon Python Internship Project Suite**.

## Overview
A modular, object-oriented console implementation of the classic Hangman word-guessing game. The application loads candidate English words from a verified dataset, filters suitable entries, displays 7 ASCII gallows stages, enforces a 6-mistake ceiling, and protects against penalties from repeated guesses and invalid inputs.

---

## Features
- **Candidate Word Dataset**: Loads from `data/words.txt` (derived from Google's 10,000 English wordlist).
- **Graceful Fallback**: If `words.txt` is missing or unreadable, an offline fallback list is seamlessly engaged.
- **7 ASCII Gallows Stages**: Accurate visual state progression from 0 mistakes (empty gallows) to 6 mistakes (complete gallows).
- **Duplicate & Invalid Input Immunity**: Repeated guesses and invalid characters (digits, symbols, multi-character strings, empty inputs) yield informative warnings without consuming attempts.
- **State Separation**: Decoupled `game_engine.py` (pure business logic), `graphics.py` (ASCII rendering), and `hangman.py` (interactive CLI).
- **Replay & Graceful Exit**: Supports continuous round replays and cleanly traps `Ctrl+C` and `EOFError`.

---

## Directory Layout
```
task1_hangman/
├── data/
│   └── words.txt            # Filtered English candidate words
├── tests/
│   └── test_hangman.py      # Automated unittest suite (18 test cases)
├── game_engine.py           # Pure Hangman state machine & guess logic
├── graphics.py              # ASCII art gallows stages & board formatter
├── hangman.py               # Interactive CLI entry point
├── word_loader.py           # Dataset loader, filter, & fallback provider
└── README.md                # Task documentation
```

---

## How to Run

### Interactive Mode
Run directly from the repository root:
```bash
python task1_hangman/hangman.py
```

### Deterministic / Automated Play
Specify a secret word directly:
```bash
python task1_hangman/hangman.py --word PYTHON
```

### Custom Dataset File
```bash
python task1_hangman/hangman.py --data-file path/to/custom_words.txt
```

---

## Automated Testing
Run the 18 automated unit tests:
```bash
python -m unittest discover -s task1_hangman/tests -p "test_*.py" -v
```
All tests are self-contained and run in under 0.1 seconds without external network dependencies.
