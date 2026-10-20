# System Architecture Specification

Datheon Python Internship Project Suite.

## Overview
The suite consists of four completely decoupled, independently executable Python applications unified by a static universal web dashboard (`index.html` / `index.htm`).

---

## Architectural Principles
1. **Decoupled Autonomy**: Each application resides in its own isolated directory (`task1_hangman/`, `task2_portfolio/`, `task3_file_organizer/`, `task4_chatbot/`) with independent entry points, datasets, and test suites.
2. **Standard Library Purity**: Core business logic relies exclusively on standard Python 3.10+ modules (`random`, `csv`, `pathlib`, `shutil`, `re`, `json`, `argparse`, `unittest`).
3. **Defense-in-Depth Filesystem Safety**: The file organizer strictly validates targets, preventing accidental operations on root or system folders.
4. **Transparent Data Modeling**: No fabricated market quotes or hallucinated bot responses; unknown states are explicitly flagged as `N/A` or fallback.
5. **Universal Static Dashboard**: Modern responsive UI styled with vanilla CSS using custom design tokens conforming to WCAG AA/AAA guidelines.

---

## Component Layout

```
internship-project-suite/
│
├── index.html                   # Universal web portal (Root dashboard)
├── README.md                    # Master documentation
├── requirements.txt             # Environment specification
├── .gitignore                   # Version control exclusions
│
├── assets/
│   ├── css/
│   │   └── styles.css           # Semantic design tokens & responsive CSS
│   └── js/
│       └── main.js              # Clipboard & navigation interactions
│
├── task1_hangman/
│   ├── hangman.py               # Interactive CLI game entry point
│   ├── game_engine.py           # Pure game state machine & guess logic
│   ├── graphics.py              # 7 ASCII gallows stages & board rendering
│   ├── word_loader.py           # Dataset filtering & fallback list
│   ├── data/
│   │   └── words.txt            # Candidate words (Google 10,000)
│   ├── tests/
│   │   └── test_hangman.py      # 18 automated unit tests
│   ├── index.html               # Task 1 dedicated project portal
│   └── README.md                # Task 1 documentation
│
├── task2_portfolio/
│   ├── portfolio.py             # Interactive CLI valuation entry point
│   ├── portfolio_calculator.py  # Financial math engine & position dataclass
│   ├── constituents_loader.py   # S&P 500 ticker validator
│   ├── price_providers.py       # Provider-independent quote interface
│   ├── csv_exporter.py          # RFC 4180 CSV persistence
│   ├── portfolio_summary.csv    # Exported portfolio valuation report
│   ├── sample_prices.json       # Offline reference quotes feed
│   ├── data/
│   │   └── constituents.csv     # S&P 500 constituent records
│   ├── tests/
│   │   └── test_portfolio.py    # 14 automated unit tests
│   ├── index.html               # Task 2 dedicated project portal
│   └── README.md                # Task 2 documentation
│
├── task3_file_organizer/
│   ├── organizer.py             # CLI file organizer entry point
│   ├── categories.py            # Category taxonomy & extension mapping
│   ├── safety_guard.py          # Root/system safety & collision handling
│   ├── logs/
│   │   └── organizer_audit.log  # Timestamped execution audit log
│   ├── tests/
│   │   └── test_organizer.py    # 12 automated unit tests (temporary sandboxes)
│   ├── index.html               # Task 3 dedicated project portal
│   └── README.md                # Task 3 documentation
│
├── task4_chatbot/
│   ├── chatbot.py               # Interactive CLI assistant entry point
│   ├── intent_classifier.py     # Rule-based regex & token scoring engine
│   ├── faq_loader.py            # FAQ JSON schema loader & fallback
│   ├── data/
│   │   └── sample_faq.json      # Verified internship FAQ dataset
│   ├── tests/
│   │   └── test_chatbot.py      # 14 automated unit tests
│   ├── index.html               # Task 4 dedicated project portal
│   └── README.md                # Task 4 documentation
│
└── docs/
    ├── ARCHITECTURE.md          # This architectural specification
    ├── DATASET_SOURCES.md       # Dataset sources & schema documentation
    └── TEST_REPORT.md           # Master QA test execution report
```
