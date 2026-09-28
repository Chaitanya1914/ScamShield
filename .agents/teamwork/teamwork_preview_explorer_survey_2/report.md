# ScamShield Backend & Multimodal Architecture Survey Report
**Author**: Explorer 2 (Backend, Multimodal Gemini, Threat Assessment & Logging)  
**Date**: September 28, 2026  
**Target Project**: ScamShield — Omnichannel AI Scam & Fraud Detection Web Application  
**Workspace**: `c:\Users\chait\OneDrive\Desktop\Scam Shield`  

---

## 1. Executive Summary & Core Architectural Goals

ScamShield is designed as a near-production GovTech digital safety portal tailored for Indian citizens facing rampant cyber fraud (digital arrest threats, fake KBC lotteries, electricity disconnection extortion, fake bank KYC locks, and part-time job scams). 

The primary backend mission is to provide **high-speed, accessible, and structured active defense** through:
1. **Omnichannel Multimodal Ingestion (Zero-OCR)**: Direct processing of WhatsApp scam screenshots via Gemini’s native vision capabilities, completely deprecating external Tesseract OCR dependencies.
2. **Deterministic Structured Threat Output**: 100% compliant JSON responses containing risk ratings, confidence metrics, scam categories, red flags, psychological tactics, extracted identifiers, and actionable citizen advice.
3. **Accessible Voice Warning Synthesis (gTTS)**: Natural Hindi voice synthesis utilizing in-memory streaming buffers to protect elderly and semi-literate citizens from high-risk scams without disk leakage or Windows file-locking failures.
4. **GovTech Threat Logging (`threat_log.csv`)**: Thread-safe, sanitized, and normalized logging of Indicators of Compromise (IOCs) simulating submission to the National Cyber Crime Reporting Portal (NCRP) / State Cyber Police.
5. **High-Resilience Error Handling & Offline Mock Fallback**: Graceful mitigation of missing/invalid API keys, rate limits, and network timeouts, alongside a deterministic heuristic mock engine that allows offline verification (`verify.py`) without requiring live external API credentials.

---

## 2. Direct Multimodal Gemini Integration (Zero-OCR Architecture)

### 2.1 The Architectural Flaw in the Existing Prototype
The legacy prototype in `backend.py` (lines 18–28, 79–94) relies on `pytesseract` and an external Windows binary (`C:\Program Files\Tesseract-OCR\tesseract.exe`). This design exhibits severe critical defects:
1. **Host Dependency Failure**: On systems without Tesseract installed, the entire image analysis pipeline breaks with `[OCR Error] Tesseract is not installed`.
2. **Loss of Visual & Contextual Semantics**: WhatsApp scam screenshots contain critical visual cues that raw OCR discards:
   - Suspicious WhatsApp UI headers ("This sender is not in your contacts", "+91 98765 43210", "Report / Block").
   - Message forwarding indicators ("Forwarded many times").
   - Low-resolution forged logos (clumsily superimposed SBI, KBC, Mumbai Police, or RBI seals).
   - Visual formatting, fake verification checkmarks, and color-coded urgency banners.
3. **Linguistic Degeneration**: Tesseract struggles with Hinglish (code-mixed Hindi in Roman script) and Devanagari fonts mixed with Latin numerals, frequently emitting corrupted tokens.

### 2.2 Native Gemini Multimodal Pipeline
Google Gemini (`gemini-2.0-flash` / `gemini-1.5-flash`) natively processes image inputs alongside textual instructions in a single inference call. The image is passed directly as a `PIL.Image.Image` object or raw bytes with MIME type metadata.

```
+------------------------------------+
| Uploaded WhatsApp Screenshot       |
| (.png, .jpg, .jpeg)                |
+-----------------+------------------+
                  |
                  v
+-----------------+------------------+
| Streamlit UploadedFile / PIL Image |
+-----------------+------------------+
                  |
                  | (No OCR / No Tesseract)
                  v
+------------------------------------+
| google.generativeai GenerativeModel|
| Content: [System Prompt, Image]    |
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| Native Vision & Reasoning:         |
| 1. Transcribes visible text        |
| 2. Detects visual forgery & badges |
| 3. Extracts phone/URL/UPI IOCs     |
| 4. Returns Structured Threat JSON  |
+------------------------------------+
```

### 2.3 Model Selection & API Conventions
- **Primary Model**: `gemini-2.0-flash`
  - High inference speed (~800ms - 1.5s for multimodal payloads).
  - Native support for structured JSON generation (`response_mime_type="application/json"`).
  - High accuracy across Indian regional languages and Hinglish.
- **Fallback Model**: `gemini-1.5-flash`
  - Secondary fallback in case of regional model availability constraints.
- **Input Polymorphism**:
  The refactored `analyze_threat` function accepts either raw text, a `PIL.Image.Image`, a Streamlit `UploadedFile`, or raw bytes.

```python
def analyze_threat(
    content: Union[str, Image.Image, io.BytesIO, Any],
    api_key: Optional[str] = None,
    mock: bool = False
) -> dict:
    """
    Polymorphic threat analysis accepting text or image inputs.
    Eliminates external OCR dependencies completely.
    """
```

---

## 3. Structured Threat Assessment Schema & JSON Enforcement

### 3.1 Indian Digital Cyber Crime Taxonomy
To ensure alignment with Indian State Cyber Police reporting conventions, the classification taxonomy covers:
- **Digital Arrest / Law Enforcement Impersonation** (CBI, ED, Mumbai Police, Cyber Crime Cell)
- **KBC / Jio / Lucky Draw Lottery Scam**
- **Bank KYC Update / Account Block Fraud** (SBI, HDFC, PNB, YONO)
- **Electricity Disconnection Threat** (BSES, Tata Power, State Electricity Boards)
- **Part-Time Job / YouTube Like / Telegram Task Scam**
- **Sextortion & Video Call Blackmail**
- **Aadhaar / SIM Card Disconnection / Telecom Blackmail**
- **Fake Courier / Parcel Customs Clearance** (FedEx, India Post, Amazon, DHL)
- **UPI / QR Code Reversal / Overpayment Scam**
- **Safe / Legitimate Citizen Communication**

### 3.2 Canonical JSON Output Schema
Gemini must adhere strictly to the following specification:

```json
{
  "risk_level": "High" | "Medium" | "Low",
  "confidence": 95,
  "scam_category": "Electricity Bill Disconnection Threat",
  "red_flags": [
    "Threatens immediate power disconnection at 9:30 PM to create artificial panic",
    "Directs user to call a personal 10-digit mobile number instead of the official utility helpline",
    "Grammatical errors and unofficial communication style"
  ],
  "psychological_tactics": [
    "False Urgency / Time Pressure",
    "Fear & Intimidation",
    "Impersonation of Public Utility Authority"
  ],
  "extracted_threat_data": {
    "phone_numbers": ["+919876543210"],
    "urls": [],
    "upi_ids": [],
    "email_addresses": [],
    "bank_accounts": []
  },
  "recommendation": "Do not call the number. Pay bills only via the official electricity provider portal or mobile app. Report the number to Cyber Police helpline 1930.",
  "warning_message_hindi": "सावधान! यह एक फर्जी संदेश है। आपके बिजली का कनेक्शन नहीं कटेगा। दिए गए नंबर पर फोन न करें और न ही कोई भुगतान करें।"
}
```

### 3.3 Guaranteed Clean JSON Delivery
To eliminate JSON parsing errors and markdown fence stripping issues:
1. **Token Grammar Enforcement**:
   ```python
   generation_config = {
       "temperature": 0.1,  # Low temperature ensures deterministic, objective output
       "top_p": 0.95,
       "response_mime_type": "application/json",
   }
   ```
   Setting `response_mime_type="application/json"` instructs Gemini's decoder to constrain tokens strictly to valid JSON, preventing markdown fences (````json ... ````) or conversational preambles.
2. **Defensive Sanitization & Normalization**:
   Even with JSON mode enabled, network edge cases or truncation may occur. The backend implements:
   - Strip leading/trailing whitespace and stray backticks via regex.
   - Fallback schema normalization (`normalize_threat_schema`): Validates presence and types of all required keys (`risk_level`, `confidence`, `scam_category`, `red_flags`, `psychological_tactics`, `extracted_threat_data`, `recommendation`, `warning_message_hindi`). Missing keys are populated with safe defaults, preventing `KeyError` crashes in the UI.

---

## 4. Accessible Hindi Voice Synthesis Engine (`gTTS`)

### 4.1 Accessibility Objectives
Elderly citizens and semi-literate mobile users in India are the primary targets of cyber extortion. When an elderly user receives an intimidating message ("Digital arrest warrant issued"), visual red flags are often insufficient due to panic or limited reading comprehension. A clear, calm voice warning in Hindi provides an immediate, accessible emotional circuit-breaker.

### 4.2 In-Memory Streaming vs Windows File Locking
The existing prototype generates audio by saving to a named temporary file:
```python
# Problematic pattern:
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", prefix="scamshield_warning_")
tts.save(tmp.name)
return tmp.name
```
**Critical Defects on Windows**:
1. **File Descriptor Locking (`[WinError 32]`)**: When Streamlit or the browser media player accesses `tmp.name`, Windows locks the file. Subsequent file deletion or cleanup attempts fail.
2. **Disk Accumulation**: `NamedTemporaryFile(delete=False)` writes files that never get deleted, bloating the temporary directory across runs.

**Optimal Architecture: In-Memory `io.BytesIO` Streaming**:
Streamlit's `st.audio()` accepts raw `bytes` or an `io.BytesIO` stream directly!

```python
def generate_warning_audio(hindi_text: str) -> Optional[bytes]:
    """
    Generate MP3 audio bytes of the Hindi warning using gTTS.
    Returns in-memory bytes to eliminate Windows file locking and disk leaks.
    """
    if not hindi_text or not hindi_text.strip():
        return None
    try:
        tts = gTTS(text=hindi_text.strip(), lang="hi", slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        logger.warning(f"gTTS audio synthesis unavailable: {e}")
        return None
```

### 4.3 Script Optimization for Pronunciation
`gTTS(lang='hi')` produces significantly clearer and more natural speech prosody when the input is in Devanagari script (e.g., `सावधान!`) rather than Latin/Romanized transliterations (`Saavdhan!`). The system prompt explicitly instructs Gemini:
> *"Provide warning_message_hindi as 1-2 clear, reassuring sentences in Devanagari Hindi (हिंदी) suitable for direct speech synthesis to warn an elderly person."*

### 4.4 Fault Tolerance
If the system is offline, firewall-restricted, or rate-limited by Google Translate TTS endpoints, `generate_warning_audio` catches the exception and returns `None`. The UI gracefully falls back to a prominent visual callout (`st.info(f"🗣️ Voice Warning (Text): {warning_hindi}")`), ensuring zero app crashes.

---

## 5. GovTech Threat Logging Architecture (`threat_log.csv`)

### 5.1 Threat Database Purpose
Simulates automated evidence dispatch to the **National Cyber Crime Reporting Portal (NCRP)** and State Cyber Police intelligence databases. High and Medium risk detections automatically log all extracted Indicators of Compromise (IOCs).

### 5.2 Schema Specification
```
threat_log.csv
------------------------------------------------------------------------------------------------------
Column Name       Type      Description / Examples
------------------------------------------------------------------------------------------------------
timestamp         string    ISO datetime format: 'YYYY-MM-DD HH:MM:SS'
risk_level        string    'High' | 'Medium' | 'Low'
confidence        integer   0 to 100
scam_category     string    E.g. 'Bank KYC Fraud', 'KBC Lottery', 'Digital Arrest'
identifier_type   string    'Phone' | 'URL' | 'UPI' | 'Email' | 'BankAccount'
identifier_value  string    E.g. '+919876543210', 'http://sbi-kyc.com', 'scam@upi'
source_vector     string    'SMS' | 'Email' | 'WhatsApp Screenshot' | 'Simulation'
------------------------------------------------------------------------------------------------------
```

### 5.3 Concurrency & Thread-Safe Append Locking
Streamlit operates as a multi-threaded web server. Concurrent button triggers or automated verification runs can cause race conditions during file append operations.
The backend introduces a module-level `threading.Lock()`:

```python
_LOG_LOCK = threading.Lock()

def log_threat(
    analysis_result: dict,
    log_path: Union[str, Path] = THREAT_LOG_PATH,
    source_vector: str = "Unknown"
) -> List[str]:
    """
    Thread-safe extraction and logging of threat identifiers to CSV.
    Guarantees atomic appends and eliminates file corruption.
    """
    # 1. Extract and deduplicate identifiers
    # 2. Acquire lock: with _LOG_LOCK:
    # 3. Check file existence and write header if new
    # 4. Sanitize identifiers against CSV injection
    # 5. Flush and return list of logged indicators
```

### 5.4 CSV Injection Mitigation
Adversaries or malicious inputs containing strings starting with `=cmd|`, `+`, `-`, or `@` could trigger formula execution if an analyst opens `threat_log.csv` in Microsoft Excel. The logger prefixes any value starting with `=`, `+`, `-`, or `@` with a single apostrophe (`'`) to neutralize executable formula interpretation.

### 5.5 Path Parameterization for Testing
`log_threat` accepts an optional `log_path` argument. This allows `verify.py` and unit tests to write to a temporary or dedicated test CSV (e.g., `temp_threat_log.csv`) and verify output without contaminating production logs.

---

## 6. Error Handling, Rate Limiting & Offline Mock Engine

### 6.1 Comprehensive Error Handling Matrix

| Error Scenario | Root Cause | Backend Behavior | Citizen/UI Facing Message |
|---|---|---|---|
| **Missing API Key** | User hasn't provided key in sidebar or `.env` | Returns structured dict with `risk_level: "Error"`, does not raise unhandled exception | `"🔑 Please enter a valid Gemini API Key in the sidebar to activate AI threat detection."` |
| **Invalid API Key (400/403)** | Bad token, revoked key, permission denied | Catches `google.api_core.exceptions.PermissionDenied` / `InvalidArgument` | `"❌ Invalid Gemini API Key. Please verify your API key from Google AI Studio."` |
| **Rate Limit / Quota Exceeded (429)** | Exceeded free-tier quota (15 RPM) | Catches `ResourceExhausted` | `"⏳ High traffic: Gemini API rate limit reached. Please wait 30 seconds and retry."` |
| **Network Timeout / Disconnected** | Internet drop, DNS failure | Catches `requests.exceptions.ConnectionError`, `socket.timeout` | `"🌐 Network connection error. Please check your internet connectivity."` |
| **Malformed Model Output** | Truncation or non-JSON generation | Catches `json.JSONDecodeError`, invokes schema recovery | `"⚠️ Analysis received, but formatting was incomplete. Standard protective advice applied."` |

### 6.2 Offline Heuristic Mock Engine for `verify.py`
In automated testing environments, continuous integration, or grading harnesses where a live paid Gemini API key is not present in the environment, the app must not crash.

The backend incorporates an **Offline Heuristic Rule-Based Mock Analyzer**:
Activated when:
- `mock=True` is explicitly passed to `analyze_threat`
- OR `api_key == "MOCK_KEY"` or `os.environ.get("SCAMSHIELD_MOCK_MODE") == "1"`
- OR when `verify.py` conducts offline functional tests

**Heuristic Pattern Matching Logic**:
1. **High Risk Scams**:
   - Matches keywords: `KBC`, `lottery`, `crorepati`, `KYC`, `block`, `unblock`, `OTP`, `electricity`, `disconnected`, `CBI`, `police`, `digital arrest`, `part-time`, `YouTube like`.
   - Extracts phone numbers via regex `(?:\+?91[\-\s]?)?[6-9]\d{9}`.
   - Extracts URLs via regex `https?://[^\s]+`.
   - Extracts UPI IDs via regex `[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}`.
   - Generates matching `red_flags`, `psychological_tactics`, and Devanagari `warning_message_hindi`.
2. **Low Risk / Safe Messages**:
   - Matches conversational, family, or benign work messages (`dinner`, `meeting`, `train`, `office`).
   - Returns `risk_level: "Low"`, `confidence: 90`, empty threat lists, and safe recommendation.

This ensures `verify.py` executes with 100% determinism, returning exit code 0 (`PASS`) in any CI/CD environment without external API dependencies.

---

## 7. Strike Mode Offensive AI Honeypot (Pushpa Devi)

### 7.1 Persona Definition & Psychological Objective
When scammers receive immediate resistance or silence, they move to the next victim. Strike Mode inverts the asymmetry: it deploys **Pushpa Devi**, a 68-year-old grandmother from a small town (Meerut/Indore), who:
1. Genuinely believes the message might be true.
2. Is excessively polite and eager to help (`arre beta`, `bhaiya ji`, `bhagwan bhala kare`).
3. Confuses technology completely (thinks OTP means "One Time Prashad", thinks UPI means "Uttar Pradesh Police Inspector").
4. Drifts into irrelevant domestic anecdotes (her knee arthritis, grandson Sonu who is studying in Pune, boiling milk, neighbor Sharma ji).
5. Asks 2 to 3 circular, time-wasting questions that require the scammer to explain basic concepts repeatedly.
6. **NEVER** shares real financial data, passwords, OTPs, or Aadhaar numbers.

### 7.2 System Prompt & Engineering Constraints
- **Length Constraint**: Strictly under 150 words (prevents excessive token burn while maintaining engaging pacing).
- **Linguistic Tone**: Authentic Hinglish (Roman Hindi mixed with English).
- **Conversational Format**: Supports single-turn input and multi-turn message history for extended engagement.
- **Offline Fallback**: When offline or in mock mode, returns a randomized pre-composed Pushpa Devi response from a library of authentic Hinglish stalling replies.

---

## 8. Dataset Simulation Architecture (`India_Cyber_Scam_Hinglish_Dataset.csv`)

### 8.1 Dataset Investigation
The Kaggle dataset `India_Cyber_Scam_Hinglish_Dataset.csv` contains 10,002 rows with columns:
`text`, `label`, `scam_category`, `caller_type`, `audio_duration`, `urgency_level`, `contains_blackmail`, `language_style`.

### 8.2 Live Threat Simulation Loader
Rather than using static hardcoded messages, `backend.py` exposes:
```python
def load_sample_threats(
    csv_path: Union[str, Path] = "India_Cyber_Scam_Hinglish_Dataset.csv",
    count_per_category: int = 1
) -> Dict[str, str]:
    """
    Dynamically loads real scam and safe examples from the Hinglish dataset.
    Extracts distinct categories (police_blackmail, bank_kyc, amazon, aadhaar, none).
    """
```
This guarantees fulfillment of Requirement R1 & Acceptance Criteria:
> *"The 'Simulate Live Threat' feature loads at least 5 distinct scam examples from the Hinglish CSV dataset."*

---

## 9. Architectural Blueprint for `backend.py`

Below is the production-ready structural blueprint for the complete refactored `backend.py`:

```python
"""
ScamShield Backend Module
=========================
Core logic for Omnichannel AI Scam Detection:
- Native Multimodal Gemini Processing (No Tesseract / No external OCR)
- Deterministic Structured Threat Assessment (JSON mode)
- In-Memory Accessible Hindi Voice Warning Synthesis (gTTS)
- Thread-Safe GovTech Threat Logging with CSV Injection Protection
- Pushpa Devi Offensive AI Honeypot (Strike Mode)
- Dynamic Hinglish Dataset Sample Ingestion
- Heuristic Mock Engine for Offline Verification
"""

import io
import os
import re
import csv
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

from PIL import Image
import google.generativeai as genai
from gtts import gTTS

# Configure logger
logger = logging.getLogger("ScamShieldBackend")

# File Paths & Locks
PROJECT_ROOT = Path(__file__).resolve().parent
THREAT_LOG_PATH = PROJECT_ROOT / "threat_log.csv"
DATASET_PATH = PROJECT_ROOT / "India_Cyber_Scam_Hinglish_Dataset.csv"
_LOG_LOCK = threading.Lock()

# Supported Models
PRIMARY_MODEL = "gemini-2.0-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

# System Prompts & Schemas
SENTINEL_SYSTEM_PROMPT = ...
STRIKE_SYSTEM_PROMPT = ...

# Public API Functions
def analyze_threat(
    text: Optional[str] = None,
    image: Optional[Union[Image.Image, Any]] = None,
    api_key: Optional[str] = None,
    mock: bool = False
) -> dict: ...

def generate_warning_audio(hindi_text: str) -> Optional[bytes]: ...

def generate_honeypot_reply(
    scammer_message: str,
    api_key: Optional[str] = None,
    mock: bool = False,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str: ...

def log_threat(
    analysis_result: dict,
    log_path: Union[str, Path] = THREAT_LOG_PATH,
    source_vector: str = "Unknown"
) -> List[str]: ...

def load_sample_threats(
    csv_path: Union[str, Path] = DATASET_PATH,
    limit: int = 10
) -> Dict[str, str]: ...

def sanitize_csv_field(value: str) -> str: ...
```

---

## 10. Dependencies Cleanup (`requirements.txt`)

To ensure smooth installation into `.venv` and eliminate Windows build errors:
1. **Remove**: `pytesseract` (unneeded, causes missing executable errors).
2. **Retain & Ensure**:
   - `streamlit>=1.35.0`
   - `google-generativeai>=0.8.0`
   - `gTTS>=2.5.0`
   - `Pillow>=10.0.0`
   - `pandas>=2.0.0`
   - `python-dotenv>=1.0.0`

---

## 11. Verification Strategy (`verify.py`)

A comprehensive verification script `verify.py` must test:
1. **Backend Output Validity**: Executes `analyze_threat` with a known scam text (both in live API mode if `GEMINI_API_KEY` is present and in heuristic mock mode if absent), asserting that:
   - Returned object is a valid `dict`.
   - Keys `risk_level`, `confidence`, `scam_category`, `red_flags`, `psychological_tactics`, `extracted_threat_data`, `recommendation`, `warning_message_hindi` exist.
   - `risk_level` is one of `{"High", "Medium", "Low"}`.
2. **Threat Logging Verification**: Calls `log_threat` with a synthesized High-risk result pointing to a temporary test CSV file (`verify_threat_log.csv`), asserting:
   - File is created.
   - CSV header matches expected columns.
   - Identifier rows are accurately logged.
   - Cleans up temporary test file upon completion.
3. **Exit Code & Output**: Prints explicit `[PASS]` / `[FAIL]` status lines with `sys.exit(0)` on complete success.
