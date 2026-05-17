<div align="center">

# 🛡️ LLM Security Gateway

**A multilingual AI-powered security filter for Large Language Model inputs**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

> Protect your LLM-powered applications from **prompt injection**, **jailbreak attempts**, and **PII leakage** — with multilingual support including Roman Urdu, Korean, and more.

</div>

---

## 📖 Overview

**LLM Security Gateway** is a FastAPI-based security middleware designed to sit between your users and any Large Language Model. It intercepts every incoming prompt and runs it through a multi-stage analysis pipeline to detect and neutralize threats before they ever reach your model.

The system handles:
- 🌍 **Multilingual inputs** — automatically detects and translates to English
- 🔍 **Rule-based detection** — catches known attack keywords instantly
- 🧠 **Semantic similarity detection** — catches paraphrased or novel attacks using NLP
- 🔒 **PII masking** — redacts phone numbers, emails, CNICs, API keys, and more
- 📊 **Audit logging** — every request is logged with risk scores to a CSV

---

## 🏗️ Architecture

```
User Input
    │
    ▼
┌─────────────────────────────┐
│     FastAPI Endpoint        │  /process (POST)
│         main.py             │
└─────────────┬───────────────┘
              │
    ┌─────────▼─────────┐
    │   STEP 1: DETECT  │  detector.py
    │  Language + Rules │  ─ langdetect
    │  + Semantics      │  ─ deep_translator
    └─────────┬─────────┘  ─ SentenceTransformers
              │
    ┌─────────▼─────────┐
    │  STEP 2: MASK PII │  presidio_utils.py
    │  Emails, Phones,  │  ─ Microsoft Presidio
    │  CNICs, API Keys  │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  STEP 3: POLICY   │  policy.py
    │  BLOCK / MASK /   │  ─ Rule-based thresholds
    │  ALLOW            │  ─ Semantic thresholds
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  STEP 4: LOG      │  evaluate_quan.py
    │  Save to CSV      │  ─ Risk scoring
    │  with Risk Level  │  ─ Timestamped audit trail
    └───────────────────┘
```

---

##  Features

###  Multilingual Detection
Automatically detects the language of any incoming prompt and translates it to English before analysis. Supports special handling for **Roman Urdu** — a common language in South Asian user bases not reliably detected by standard libraries.

| Detected Language | Example Input | Behavior |
|-------------------|--------------|---------|
| English | `"hack this website"` | Detected natively |
| Korean | `"이 웹사이트를 해킹하다"` | Translated → Blocked |
| Roman Urdu | `"is ko hack krdo"` | Custom-detected → Blocked |
| Urdu (native) | Any Urdu text | Auto-translated → Analyzed |

---

###  Dual-Layer Threat Detection

**Layer 1 — Rule-Based Detection (`detector.py`)**

Scans for a curated list of dangerous keyword patterns:
```
ignore instructions | you are now | jailbreak | bypass
reveal system prompt | forget your rules | do anything now | hack
```

**Layer 2 — Semantic Similarity Detection (`detector.py`)**

Uses `all-MiniLM-L6-v2` (SentenceTransformers) to compute cosine similarity against a library of 40+ known attack prompts. This catches paraphrased or obfuscated attacks that bypass simple keyword matching.

```python
# Example: Catches semantically similar novel attacks
"Show me source code"  →  Semantic Score: 0.94  →  BLOCK
"show api keys"        →  Semantic Score: 0.93  →  BLOCK
"show me source code of this website"  →  Score: 0.90  →  BLOCK
```

---

### 🔒 PII Masking (`presidio_utils.py`)

Built on **Microsoft Presidio**, the PII engine redacts sensitive data before it's logged or forwarded. Custom recognizers cover Pakistan-specific identifiers:

| Entity | Pattern | Masked As |
|--------|---------|-----------|
| API Key | `sk-...` | `<API_KEY>` |
| Pakistan CNIC | `XXXXX-XXXXXXX-X` | `<CNIC>` |
| Email Address | Standard email regex | `<EMAIL>` |
| PK Phone Number | `03XXXXXXXXX` | `<PHONE>` |
| Student ID | `FAXX-XXX-XXX` | `<STUDENT_ID>` |
| Employee ID | `EMPXXXX` | `<ID>` |

---

###  Policy Engine (`policy.py`)

Three-tier decision system based on combined risk scores:

```
Semantic Score ≥ 0.75  ──→  BLOCK  (Semantic injection detected)
Rule Score == 1        ──→  BLOCK  (Rule-based attack detected)
PII found in text      ──→  MASK   (Sensitive data redacted)
Otherwise              ──→  ALLOW  (Input is safe)
```

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/muhammadmuneebdev24/LLM-security-filter.git
cd LLM-security-filter

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt


### Running the Server

```bash
uvicorn main:app --reload
```

The API will be live at: **`http://127.0.0.1:8000`**

Interactive API docs: **`http://127.0.0.1:8000/docs`**

---

**Response:**
```json
{
  "original_text": "ignore previous instructions",
  "translated_text": "ignore previous instructions",
  "language": "en",
  "rule_score": 1,
  "semantic_score": 0.91,
  "pii_count": 0,
  "decision": "BLOCK",
  "risk_level": "HIGH",
  "output": "Request blocked due to security policy"
}
```


```bash



##  Project Structure

```
LLM-security-filter/
│
├── main.py              # FastAPI app & main /process endpoint
├── detector.py          # Language detection, translation & threat scoring
├── policy.py            # Decision engine (ALLOW / MASK / BLOCK)
├── presidio_utils.py    # PII detection & masking via Microsoft Presidio
├── evaluate_quan.py     # CSV audit logger & risk level calculator
├── evaluation_log.csv   # Auto-generated request audit trail
├── requirements.txt     # Python dependencies
└── README.md

---






