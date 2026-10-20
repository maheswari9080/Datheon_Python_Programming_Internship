# Task 04: Rule-Based Interactive Terminal FAQ Assistant

Part of the **Datheon Python Internship Project Suite**.

## Overview
A lightweight, deterministic conversational assistant designed to answer internship questions based on a verified knowledge base (`data/sample_faq.json`). Built purely with Python standard library modules (`re`, `json`, `string`), avoiding heavy external NLP frameworks or paid AI APIs.

---

## Intent Taxonomy & Scoring Strategy
The assistant applies a strict hierarchy and token scoring engine (Jaccard similarity with specific term boosting):
1. **System Commands**: `help`, `commands`, `exit`, `quit`, `bye` evaluate immediately with 100% confidence.
2. **Greetings**: Recognizes standard greetings (`hello`, `hi`, `good morning`). If paired with an inquiry (e.g., "Hello, what are your hours?"), it fulfills the question directly.
3. **Specific Question Priority**: Exact questions score 1.0; questions containing high-information keywords (`hours`, `submit`, `certificate`) receive specificity boosts over generic matches.
4. **Unsupported Queries**: Explicitly informs the user when information (such as pricing or billing) is unavailable in the dataset, rather than fabricating details.
5. **Safe Fallback**: When input confidence falls below threshold, the assistant acknowledges the unknown query and lists verified questions it can answer.

---

## Dataset Schema
Adheres strictly to `sample_faq.json`:
```json
{
  "greetings": ["hello", "hi", "hey", "..."],
  "faqs": [
    {
      "question": "What are your hours of operation?",
      "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
    }
  ]
}
```

---

## How to Run

### Interactive Console Mode
```bash
python task4_chatbot/chatbot.py
```

### Non-Interactive Single Query Mode
```bash
python task4_chatbot/chatbot.py --query "When will I receive my certificate?"
```

### Custom FAQ File
```bash
python task4_chatbot/chatbot.py --data-file path/to/custom_faq.json
```

---

## Automated Testing
Run the 14 automated unit tests:
```bash
python -m unittest discover -s task4_chatbot/tests -p "test_*.py" -v
```
All tests verify intent classification, schema validation, fallback safety, and non-fabrication offline.
