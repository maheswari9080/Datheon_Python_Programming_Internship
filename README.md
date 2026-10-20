# Python Internship Project Suite

Datheon Python Internship — Four Independent Python Applications + Universal Web Dashboard.

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-58%20passed-brightgreen)](docs/TEST_REPORT.md)
[![Status](https://img.shields.io/badge/build-passing-brightgreen)](docs/TEST_REPORT.md)

---

## License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

---

## Suite Purpose & Overview
This repository contains four completely decoupled, production-grade Python applications demonstrating core software engineering capabilities: algorithmic problem-solving, financial data processing, filesystem automation, and deterministic conversational AI. All projects are unified through an accessible developer portal dashboard (`index.html`).

---

## Repository Structure
```
internship-project-suite/
│
├── index.html                   # Universal web portal (Root dashboard)
├── README.md                    # Master documentation (this file)
├── requirements.txt             # Dependency specification
├── .gitignore                   # Version control exclusions
│
├── assets/                      # Shared assets for web portal
│   ├── css/styles.css           # Design tokens (design-colorize compliant)
│   └── js/main.js               # Interactive clipboard & UI scripts
│
├── task1_hangman/               # Task 01: Hangman Console Game
│   ├── hangman.py               # Interactive CLI game controller
│   ├── game_engine.py           # Pure game state machine & rules
│   ├── graphics.py              # 7 ASCII gallows stages & board rendering
│   ├── word_loader.py           # Candidate word loader & fallback
│   ├── data/words.txt           # Filtered Google 10,000 words dataset
│   ├── tests/test_hangman.py    # 18 automated unit tests
│   ├── index.html               # Task 1 web project portal
│   └── README.md                # Task 1 documentation
│
├── task2_portfolio/             # Task 02: Stock Portfolio Performance Tracker
│   ├── portfolio.py             # Interactive CLI valuation tool
│   ├── portfolio_calculator.py  # Financial math engine & dataclasses
│   ├── constituents_loader.py   # S&P 500 constituent validator
│   ├── price_providers.py       # Provider-independent pricing interface
│   ├── csv_exporter.py          # RFC 4180 CSV persistence
│   ├── portfolio_summary.csv    # Exported portfolio valuation report
│   ├── sample_prices.json       # Offline reference quotes feed
│   ├── data/constituents.csv    # S&P 500 company constituent records
│   ├── tests/test_portfolio.py  # 14 automated unit tests
│   ├── index.html               # Task 2 web project portal
│   └── README.md                # Task 2 documentation
│
├── task3_file_organizer/        # Task 03: Automated File Organizer
│   ├── organizer.py             # CLI file organizer
│   ├── categories.py            # Category taxonomy & extension mapping
│   ├── safety_guard.py          # Root/system safety & collision handling
│   ├── logs/organizer_audit.log # Detailed audit log
│   ├── tests/test_organizer.py  # 12 automated unit tests (temporary sandboxes)
│   ├── index.html               # Task 3 web project portal
│   └── README.md                # Task 3 documentation
│
├── task4_chatbot/               # Task 04: Rule-Based FAQ Assistant
│   ├── chatbot.py               # Interactive CLI conversational loop
│   ├── intent_classifier.py     # Rule-based regex & token scoring engine
│   ├── faq_loader.py            # FAQ JSON schema adapter & fallback
│   ├── data/sample_faq.json     # Verified internship FAQ dataset
│   ├── tests/test_chatbot.py    # 14 automated unit tests
│   ├── index.html               # Task 4 web project portal
│   └── README.md                # Task 4 documentation
│
└── docs/                        # Suite-wide technical documentation
    ├── ARCHITECTURE.md          # In-depth architectural specification
    ├── DATASET_SOURCES.md       # Dataset sources & schema documentation
    └── TEST_REPORT.md           # Master QA test execution report
```

---

## Python Version & Requirements
- **Python Version**: Python 3.10, 3.11, or 3.12.
- **Core Dependencies**: None. All core applications rely exclusively on Python standard library modules (`random`, `csv`, `pathlib`, `shutil`, `re`, `json`, `argparse`, `unittest`).
- **Optional Dependencies**:
  - `yfinance`: Optional live stock quote fetching for Task 2. The tracker works fully offline without it.

---

## Verified Datasets & Provenance
| Project | Dataset | Source URL | Verified Local File |
| :--- | :--- | :--- | :--- |
| **01 Hangman** | English Words | [Google 10k English](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt) | `task1_hangman/data/words.txt` |
| **02 Portfolio** | S&P 500 Constituents | [DataHub Constituents](https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv) | `task2_portfolio/data/constituents.csv` |
| **03 Organizer** | Python `shutil` Docs | [Python Library Documentation](https://docs.python.org/3/library/shutil.html) | Configurable taxonomy |
| **04 Chatbot** | Internship FAQ | [Datheon FAQ Dataset](https://www.datheon.in/datasets/sample_faq.json) | `task4_chatbot/data/sample_faq.json` |

*Every task includes structured offline fallback data, guaranteeing seamless execution even in air-gapped environments.*

---

## Execution Guide

### Task 01: Hangman Console Game
```bash
# Interactive play
python task1_hangman/hangman.py

# Deterministic test mode
python task1_hangman/hangman.py --word PYTHON
```

### Task 02: Stock Portfolio Performance Tracker
```bash
# Interactive menu mode
python task2_portfolio/portfolio.py

# Non-interactive demo mode (outputs ASCII table and exports CSV)
python task2_portfolio/portfolio.py --demo
```

### Task 03: Automated File Organizer
```bash
# Dry-run simulation (preview moves without touching files)
python task3_file_organizer/organizer.py --target "C:\Users\YourName\Downloads" --dry-run

# Live organization
python task3_file_organizer/organizer.py --target "C:\Users\YourName\Downloads"
```

### Task 04: Rule-Based Interactive Chatbot
```bash
# Interactive conversational session
python task4_chatbot/chatbot.py

# Single-query testing
python task4_chatbot/chatbot.py --query "What are your hours of operation?"
```

---

## Running the Automated Test Suites
Run the entire 58-test suite across all four applications:
```bash
# Task 1 Hangman (18 tests)
python -m unittest discover -s task1_hangman/tests -p "test_*.py" -v

# Task 2 Portfolio (14 tests)
python -m unittest discover -s task2_portfolio/tests -p "test_*.py" -v

# Task 3 File Organizer (12 tests)
python -m unittest discover -s task3_file_organizer/tests -p "test_*.py" -v

# Task 4 FAQ Chatbot (14 tests)
python -m unittest discover -s task4_chatbot/tests -p "test_*.py" -v
```

---

## Opening the Web Dashboard
Open `index.html` directly in any modern browser:
```powershell
# Windows PowerShell
Start-Process "index.html"

# Or on macOS / Linux
# open index.html  # macOS
# xdg-open index.html  # Linux
```
The universal dashboard works entirely client-side with zero local server requirement.

---

## Portfolio Pricing & Educational Disclaimer
- `constituents.csv` contains S&P 500 company directory metadata, **not** real-time pricing feeds.
- Valuation pricing is provider-independent: uses offline reference quotes (`sample_prices.json`), manual user input, or optional `yfinance` live fetching.
- **Disclaimer**: This software is strictly for academic and educational evaluation. It does not provide financial or investment advice.

---

## File Organizer Safety Protocol
- Strictly refuses to organize filesystem roots (`C:\`, `/`), operating system directories (`System32`, `Program Files`, `/bin`), and the project repository directory itself.
- Re-running the utility never creates recursive nested category folders.
- Conflicts are handled safely without silent data loss via configurable collision policies (`rename`, `skip`, `overwrite`).
