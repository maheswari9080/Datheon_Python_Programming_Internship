# Master QA Test Execution Report

Datheon Python Internship Project Suite.

## Executive Summary
This document provides complete verification records for all four applications in the suite. All automated tests were executed using Python's built-in `unittest` runner on Python 3.11 with zero external test runners or mock libraries required.

- **Total Test Cases**: 58
- **Passing**: 58 (100%)
- **Failing**: 0 (0%)
- **Errors**: 0 (0%)
- **Execution Time**: ~0.08 seconds across all 4 suites

---

## Task 01: Hangman Console Game
- **Test File**: `task1_hangman/tests/test_hangman.py`
- **Execution Command**:
  ```bash
  python -m unittest discover -s task1_hangman/tests -p "test_*.py" -v
  ```
- **Results**: 18 Tests Passed (0.015s)
  1. `test_gallows_stages_bound` &mdash; Validates all 7 ASCII gallows stages.
  2. `test_render_board_contains_elements` &mdash; Validates formatted display of word, attempts, and letters.
  3. `test_correct_guess_reveals_position` &mdash; Validates secret word character unmasking.
  4. `test_defeat_condition_at_six_mistakes` &mdash; Validates game termination when reaching 6 mistakes.
  5. `test_duplicate_correct_guess_no_penalty` &mdash; Confirms repeat correct guesses do not penalize.
  6. `test_duplicate_guess_no_penalty` &mdash; Confirms repeat incorrect guesses do not penalize.
  7. `test_incorrect_guess_penalizes_attempt` &mdash; Confirms incorrect guesses decrement attempts by exactly 1.
  8. `test_initial_state` &mdash; Confirms 6 initial attempts and empty guess tracking.
  9. `test_invalid_input_no_penalty` &mdash; Confirms digits, symbols, and multi-character inputs do not decrement attempts.
  10. `test_victory_condition` &mdash; Confirms win state when all letters are guessed.
  11. `test_empty_input_rejected` &mdash; Enforces rejection of whitespace-only input.
  12. `test_multi_char_input_rejected` &mdash; Enforces single-character input rules.
  13. `test_non_alpha_rejected` &mdash; Enforces alphabetic input rules.
  14. `test_valid_lowercase_letter` &mdash; Validates uppercase normalization.
  15. `test_valid_whitespace_padded_letter` &mdash; Validates trimming and normalization.
  16. `test_load_existing_dataset` &mdash; Validates loading 8,076 candidate words.
  17. `test_load_malformed_file_filters_invalid_lines` &mdash; Verifies non-alpha lines are safely filtered out.
  18. `test_load_missing_file_returns_fallback` &mdash; Confirms seamless engagement of offline fallback list.

---

## Task 02: Stock Portfolio Performance Tracker
- **Test File**: `task2_portfolio/tests/test_portfolio.py`
- **Execution Command**:
  ```bash
  python -m unittest discover -s task2_portfolio/tests -p "test_*.py" -v
  ```
- **Results**: 14 Tests Passed (0.014s)
  1. `test_educational_disclaimer_present` &mdash; Validates mandatory academic disclaimer.
  2. `test_export_creates_valid_csv` &mdash; Verifies CSV output and RFC 4180 fieldnames.
  3. `test_known_ticker_lookup` &mdash; Validates S&P 500 company constituent lookup.
  4. `test_unknown_ticker_lookup` &mdash; Verifies graceful handling of non-constituent symbols.
  5. `test_invalid_negative_price_raises_error` &mdash; Rejects negative purchase price.
  6. `test_invalid_negative_quantity_raises_error` &mdash; Rejects negative share quantities.
  7. `test_invalid_zero_buy_price_raises_error` &mdash; Rejects zero purchase price.
  8. `test_invalid_zero_quantity_raises_error` &mdash; Rejects zero share quantity.
  9. `test_loss_making_position` &mdash; Validates $(C-P) \times Q$ and $\% = \frac{C-P}{P} \times 100$ on losses.
  10. `test_profitable_position` &mdash; Validates returns on gains.
  11. `test_unpriced_position_returns_none` &mdash; Asserts unquoted holdings do not fabricate prices.
  12. `test_complete_portfolio` &mdash; Validates multi-position portfolio aggregation.
  13. `test_empty_portfolio` &mdash; Validates empty holding calculations.
  14. `test_partial_portfolio_flags_incomplete` &mdash; Flags `is_complete_valuation = False` when unquoted positions exist.

---

## Task 03: Automated File Organizer
- **Test File**: `task3_file_organizer/tests/test_organizer.py`
- **Execution Command**:
  ```bash
  python -m unittest discover -s task3_file_organizer/tests -p "test_*.py" -v
  ```
- **Results**: 12 Tests Passed (0.024s)
  1. `test_code_extensions` &mdash; Categorizes `.py`, `.js`, `.json` to `Code`.
  2. `test_document_extensions` &mdash; Categorizes `.pdf`, `.docx`, `.txt` to `Documents`.
  3. `test_image_extensions` &mdash; Categorizes `.jpg`, `.png`, `.svg` to `Images`.
  4. `test_other_unsupported_extensions` &mdash; Categorizes unmapped extensions to `Other`.
  5. `test_dry_run_does_not_move_files` &mdash; Proves `--dry-run` leaves disk untouched.
  6. `test_live_move_categorizes_correctly` &mdash; Proves live moves place files in proper category folders.
  7. `test_rerun_does_not_reorganize_subfolders` &mdash; Proves existing category folders are skipped.
  8. `test_collision_rename_policy` &mdash; Appends `_1` when destination filename exists.
  9. `test_collision_skip_policy` &mdash; Skips file when `skip` collision policy is chosen.
  10. `test_reject_filesystem_root` &mdash; Safety guard refuses `C:\` or `/`.
  11. `test_reject_nonexistent_directory` &mdash; Rejects missing target directories.
  12. `test_reject_project_root` &mdash; Rejects target matching the internship project root repository.

---

## Task 04: Rule-Based Interactive Chatbot
- **Test File**: `task4_chatbot/tests/test_chatbot.py`
- **Execution Command**:
  ```bash
  python -m unittest discover -s task4_chatbot/tests -p "test_*.py" -v
  ```
- **Results**: 14 Tests Passed (0.030s)
  1. `test_certificate_faq_response_from_dataset` &mdash; Verifies certificate response from dataset.
  2. `test_empty_message_handled` &mdash; Handles empty user messages gracefully.
  3. `test_exit_intent` &mdash; Recognizes `bye`, `exit`, `quit`.
  4. `test_greeting_intent` &mdash; Recognizes `hello`, `hi`, `good morning`.
  5. `test_help_intent` &mdash; Displays available commands and FAQ topics.
  6. `test_hours_faq_response_from_dataset` &mdash; Returns operating hours from dataset.
  7. `test_submission_faq_response_from_dataset` &mdash; Returns submission instructions from dataset.
  8. `test_unknown_question_graceful_fallback` &mdash; Gracefully handles out-of-domain questions without fabricating answers.
  9. `test_unsupported_pricing_acknowledged_not_fabricated` &mdash; Acknowledges lack of pricing data instead of inventing fees.
  10. `test_load_default_dataset` &mdash; Confirms verified `sample_faq.json` loading.
  11. `test_malformed_json_activates_fallback` &mdash; Proves corrupt JSON engages offline fallback safely.
  12. `test_missing_file_activates_fallback` &mdash; Proves missing JSON engages fallback safely.
  13. `test_lowercase_and_strip` &mdash; Normalizes whitespace and casing.
  14. `test_punctuation_removal` &mdash; Strips punctuation for clean tokenization.
