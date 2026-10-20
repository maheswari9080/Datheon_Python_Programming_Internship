# Dataset Sources & Provenance Specification

Datheon Python Internship Project Suite.

## Overview
This document records the exact URLs, local storage locations, download verification results, schema structures, and fallback mechanisms implemented across all data-driven tasks.

---

## 1. Task 01: English Candidate Wordlist
- **Canonical URL**: `https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt`
- **Local Target**: `task1_hangman/data/words.txt`
- **Download Status**: HTTP 200 OK (Downloaded 75,153 bytes).
- **Inspection Findings**:
  - Plaintext format, one word per line.
  - Contains mixed-case and non-letter entries in raw state.
  - `word_loader.py` filters alphabetic words between 4 and 10 characters in length, converting to uppercase.
  - Produces 8,076 verified candidate words.
- **Offline Fallback**:
  - If `words.txt` is missing or unreadable, `word_loader.py` seamlessly falls back to `FALLBACK_WORDS` (12 programming-themed words).

---

## 2. Task 02: S&P 500 Company Constituents
- **Canonical URL**: `https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv`
- **Local Target**: `task2_portfolio/data/constituents.csv`
- **Download Status**: HTTP 200 OK (Downloaded 53,620 bytes).
- **Inspection Findings**:
  - RFC 4180 CSV format.
  - Headers: `Symbol,Security,GICS Sector,GICS Sub-Industry,Headquarters Location,Date added,CIK,Founded`
  - Total records: 503 active corporate constituents.
  - **Critical Note**: This dataset contains company information, NOT real-time pricing feeds.
- **Pricing Strategy & Fallback**:
  - Provider-independent pricing implemented in `price_providers.py`.
  - Offline reference quotes: `task2_portfolio/sample_prices.json` (14 blue-chip tickers).
  - Manual price entry supported via interactive CLI.
  - Optional live quotes via `yfinance` if installed.
  - Unpriced holdings are explicitly marked `N/A` without fabricated estimates.

---

## 3. Task 03: File Organizer Taxonomy
- **Reference Documentation**: `https://docs.python.org/3/library/shutil.html`
- **Local Implementation**: `task3_file_organizer/categories.py`
- **Supported Categories (8 + Other)**:
  - **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`
  - **Videos**: `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`
  - **Audio**: `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`
  - **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
  - **Code**: `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.c`, `.cpp`, `.json`, `.xml`
  - **Spreadsheets**: `.csv`, `.xls`, `.xlsx`, `.ods`
  - **Presentations**: `.ppt`, `.pptx`, `.odp`
  - **Other**: Unrecognized extensions or extensionless files.

---

## 4. Task 04: Internship FAQ Dataset
- **Canonical URL**: `https://www.datheon.in/datasets/sample_faq.json`
- **Local Target**: `task4_chatbot/data/sample_faq.json`
- **Download Status**: HTTP 200 OK (Downloaded 610 bytes).
- **Inspection Findings**:
  - JSON format with two top-level keys:
    - `"greetings"`: Array of 5 greeting phrases.
    - `"faqs"`: Array of 3 objects with `"question"` and `"answer"`.
- **Offline Fallback**:
  - `faq_loader.py` provides `FALLBACK_FAQ_DATA` if the JSON file is missing or contains invalid syntax.
