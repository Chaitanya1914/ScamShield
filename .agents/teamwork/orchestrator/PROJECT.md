# Project: ScamShield — Production AI Scam Detection Platform

## Architecture
- **Language & Runtime**: Python 3.11.9 (`.venv`) on Windows
- **Detection Philosophy**: Self-Sufficient Local ML as PRIMARY (Zero API Keys) + Gemini Multimodal Vision as OPTIONAL Secondary.
- **Core Modules**:
  - `scam_detector.py`: High-performance local ML engine trained on `India_Cyber_Scam_Hinglish_Dataset.csv` (10,001 rows: 5,000 safe, 5,001 scam across 7 categories). Features: TF-IDF (1,2 ngrams) + 12 hand-crafted domain signal features. Classifiers: Calibrated Logistic Regression (binary, >99% CV-accuracy) + Calibrated Multi-Class Classifier (7 categories + safe). Obfuscation-resistant IoC extractors (phone, UPI, URL). Auto-loads `scamshield_model.pkl`, auto-retrains if corrupted, and provides non-crashing heuristic fallback.
  - `backend.py`: Production-grade API layer exposing `analyze_threat(text=..., image=...) -> dict`. Routes all text inputs directly to local ML with ZERO API keys required and ZERO internet connection. Relegates Gemini API strictly to an OPTIONAL secondary layer for (a) WhatsApp screenshot multimodal vision and (b) Strike Mode conversational honeypot. In-memory `gTTS` Hindi voice warning synthesis (`io.BytesIO`). Thread-safe threat logging with CWE-1236 CSV injection protection (`threat_log.csv`).
  - `app.py`: Streamlit frontend with zero CSS contrast bugs in both light and dark themes. High-contrast government-portal theme (Navy `#0b3b60` / Slate `#f8fafc` / clean white cards). API key loaded exclusively from `.env` via `python-dotenv` (zero frontend input fields). Sidebar displays live ML metrics card (CV accuracy, F1-score, dataset size, engine status) and Cloud API status. Sentinel Mode displays source badge (`🛡️ Local ML Engine (Offline)` vs `☁️ Gemini Multimodal Vision API (Cloud)`). Strict "Rahul" persona consistency everywhere.
  - `tests/test_suite.py`: Comprehensive test suite containing 31 discrete programmatic tests validating ML cv-accuracy ≥90%, 5 known scams as High risk, 5 safe messages as Low risk, IoC extraction (phone, UPI, URL ≥3 each), threat logging with CSV injection defense, Hindi voice synthesis, and app import validation with zero API keys. Exits 0 on success, 1 on failure.
  - `requirements.txt`: Complete package manifest including `scikit-learn`, `scipy`, `numpy`, `joblib`, `streamlit`, `google-generativeai`, `gTTS`, `Pillow`, `pandas`, and `python-dotenv`.
  - `README.md`: Professional enterprise documentation with ASCII architecture diagram, quickstart, API documentation, ML benchmarks, and security model.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Local ML Model Serialization & Auto-Load | `scamshield_model.pkl` loaded on startup; metadata (accuracy, F1, timestamp) exposed via `get_metrics()` | M1 | R1 |
| 2 | Offline Text Analysis (Zero API Keys) | All text messages analyzed locally via `scam_detector.py` with >99% accuracy; zero API keys or internet needed | M1 | R1 |
| 3 | Calibrated Risk Scoring & Category Prediction | High/Medium/Low risk scoring and 7 scam category predictions (bank_kyc, police_digital_arrest, etc.) | M1 | R1 |
| 4 | Obfuscation-Resistant IoC Regex Extractors | Indian phone numbers (handles dots, spaces, +91, 0), strict UPI VPAs, and defanged URLs | M1 | R1, R3 |
| 5 | Enterprise Public API Contract | `analyze_threat(text=..., image=...) -> dict` with normalized schema and `detection_source` field | M1 | R4, R5 |
| 6 | Optional Multimodal Vision Secondary Layer | Gemini API used for WhatsApp screenshot images without OCR; deterministic mock fallback if key absent | M1 | R1, R5 |
| 7 | Secure Threat Intelligence Logging | Thread-safe logging to `threat_log.csv` with formula injection mitigation (CWE-1236) | M1 | R4, R5 |
| 8 | In-Memory Hindi Voice Warnings (gTTS) | Zero-API, in-memory `io.BytesIO` speech synthesis for High/Medium threats without file locking | M1 | R2, R3 |
| 9 | Rahul Conversational Honeypot | Strike Mode prompt & mock responses using 21yo college student 'Rahul' (zero 'Pushpa Devi' mentions) | M1, M2 | R2, R3 |
| 10 | Fault-Tolerant Model Lifecycle | Auto-retrains on corrupted pickle, falls back to rule-based engine on missing dataset | M1 | R4 |
| 11 | Zero Contrast/Readability UI Bugs | Streamlit UI high-contrast cards and text readable in both light and dark mode; `.streamlit/config.toml` | M2 | R2 |
| 12 | Secure .env-Only API Key Management | API key loaded strictly via `python-dotenv` from `.env`; zero frontend input fields | M2 | R2 |
| 13 | Sidebar ML Model Performance Metrics | Real-time display of ML accuracy, F1-score, sample count, and engine status in sidebar | M2 | R2 |
| 14 | Detection Engine Origin Indicator | Clear visual badge indicating `🛡️ Local ML Engine (Offline)` vs `☁️ Gemini Multimodal API` | M2 | R1, R2 |
| 15 | Omnichannel Tabs & Sentinel Dashboard | Tabs for Text, Screenshot Upload, and Live Threat Simulator with clean cards & auto-playing Hindi warning | M2 | R1, R2 |
| 16 | Strike Mode Chat Bubble Interface | Interactive multi-turn chat interface using `st.chat_message` for Rahul persona | M2 | R2 |
| 17 | Comprehensive Test Suite (`test_suite.py`) | 31 programmatic tests verifying ML accuracy, 5 scam / 5 safe, IoC regex, threat logging, voice, imports | M3 | R3 |
| 18 | Production Dependencies & Manifest | `requirements.txt` containing all required packages (scikit-learn, scipy, joblib, numpy, etc.) | M3 | R4 |
| 19 | Architecture & Deployment Documentation | Production `README.md` with ASCII architecture diagram, quickstart, ML benchmarks, security | M3 | R4 |
| 20 | Dual-Track End-to-End Verification | 100% test suite pass rate and forensic integrity audit pass | M4 | Final |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Backend Integration & Local ML Primary | `scam_detector.py`, `backend.py`: Wire local ML as primary engine for text, Gemini as secondary for vision/honeypot, IoC regex upgrades, schema normalization, threat logging with CSV injection protection, clean legacy docstring | none | IN_PROGRESS |
| M2 | Professional Streamlit UI Polish | `app.py`, `.streamlit/config.toml`: Fix all contrast bugs in light/dark mode, remove frontend API key input, sidebar ML metrics card, engine origin badges, Rahul persona consistency | M1 | IN_PROGRESS |
| M3 | Comprehensive Test Suite & Documentation | `tests/test_suite.py`, `requirements.txt`, `README.md`: 31 test cases, explicit PASS/FAIL, exit 0/1, full dependency manifest, production README | M1 | IN_PROGRESS |
| M4 | Final Acceptance & Forensic Audit Gate | Run `python tests/test_suite.py` & `python verify.py`, Reviewers, Challengers, Forensic Auditor pass | M1, M2, M3 | PLANNED |

## Interface Contracts
### `backend.py` ↔ Consumers (`app.py`, `tests/test_suite.py`, `verify.py`)
```python
def analyze_threat(
    text: Optional[str] = None,
    image: Optional[Union[Image.Image, bytes, str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes input text or image. Returns normalized dictionary:
    {
        "risk_level": "High" | "Medium" | "Low",
        "confidence_score": float (0.0 to 1.0),
        "confidence": int (0 to 100),
        "scam_category": str,
        "red_flags": List[str],            # Empty list [] for Low risk
        "psychological_tactics": List[str],# Empty list [] for Low risk
        "extracted_identifiers": {
            "phone_numbers": List[str],
            "upi_ids": List[str],
            "urls": List[str]
        },
        "recommended_action": str,
        "detection_source": "local_ml" | "gemini_multimodal" | "offline_fallback",
        "raw_response": Optional[str]
    }
    """
```

### `scam_detector.py` ↔ `backend.py` & `app.py`
```python
class ScamDetectorML:
    def predict(self, text: str) -> Dict[str, Any]: ...
    def get_metrics(self) -> Dict[str, Any]: ...
    def train(self) -> Dict[str, Any]: ...
```

### Threat Logging Contract (`threat_log.csv`)
- Header: `timestamp,source_channel,risk_level,confidence_score,scam_category,identifier_type,identifier_value`
- All string values starting with `=`, `+`, `-`, `@`, `\t`, `\r` must be escaped with a leading `'`.

## Code Layout & Write Boundaries
- `backend.py`, `scam_detector.py`: Owned exclusively by Worker M1.
- `app.py`, `.streamlit/config.toml`: Owned exclusively by Worker M2.
- `tests/test_suite.py`, `requirements.txt`, `README.md`: Owned exclusively by Worker M3.
