# Project: ScamShield

## Architecture
- **Language & Runtime**: Python 3.11.9 (`.venv`) on Windows
- **Core Modules**:
  - `backend.py`: All computational logic, Gemini API interactions (multimodal without OCR), structured JSON schemas, in-memory `gTTS` audio synthesis, CSV threat logging, Pushpa Devi honeypot prompt generation, dynamic dataset sampling, and offline mock fallbacks.
  - `app.py`: Streamlit frontend implementing an official National Cyber Crime Reporting Portal (NCRP) / State Cyber Police aesthetic (Navy `#0b3b60` / Slate `#f8fafc` / clean white cards), Omnichannel tabs, Sentinel dashboard, Strike Mode chat-bubbles, alert banners, and API key management.
  - `verify.py`: Standalone CLI verification script testing `backend.py` threat analysis and CSV logging, outputting explicit PASS/FAIL.
  - `requirements.txt`: Python package manifest strictly excluding `pytesseract` and external OCR binaries.
- **Data Flow**:
  1. User/Tester inputs SMS/Email text, WhatsApp Screenshot (PIL Image), or loads from `India_Cyber_Scam_Hinglish_Dataset.csv`.
  2. Input dispatched to `backend.analyze_threat()`. If API key present, calls Gemini API (`gemini-2.0-flash` / `gemini-1.5-flash`) with structured JSON schema; otherwise uses deterministic offline mock pattern engine for automated tests.
  3. If Sentinel Mode: displays structured threat metrics. If High/Medium risk, `backend.generate_voice_warning()` produces Hindi audio via `gTTS` (in-memory BytesIO) and `backend.log_threat()` appends IoCs to `threat_log.csv`. State Cyber Police alert banner is displayed in `app.py`.
  4. If Strike Mode: input passed to `backend.generate_honeypot_reply()`. Returns Hinglish response in Pushpa Devi persona, rendered in `st.chat_message` chat-bubble format with multi-turn support.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Python Environment & Clean Dependencies | Setup `.venv`, install packages (streamlit, google-generativeai, gTTS, Pillow, pandas, python-dotenv), remove pytesseract | M1 | survey |
| 2 | Multimodal Gemini Analysis (Zero OCR) | Direct PIL Image / text analysis in `backend.py` via Gemini API without OCR | M1 | survey / R1 |
| 3 | Structured Threat Assessment Schema | Strict JSON response format (risk_level, confidence, category, red_flags, psychological_tactics, extracted_identifiers, recommended_action) | M1 | survey / R2 |
| 4 | Offline Mock Fallback Engine | Deterministic fallback analysis in `backend.py` for automated tests without API keys | M1 | survey / verify.py |
| 5 | Thread-Safe Threat Logging | Thread-safe append to `threat_log.csv` with CSV formula injection mitigation and IoC extraction | M1 | survey / R4 |
| 6 | In-Memory Hindi Voice Warning (gTTS) | Accessible Hindi voice warning synthesis using `io.BytesIO` to prevent Windows file-lock errors | M1 | survey / R2 |
| 7 | Rahul / Honeypot Persona Generation | Conversational Hinglish stall tactics by confused young user/college student named 'Rahul' with anti-exfiltration boundaries | M1 | survey / R3 / update |
| 8 | Live Threat Simulator from Dataset | Dynamic sampler from `India_Cyber_Scam_Hinglish_Dataset.csv` covering ≥5 distinct scam categories | M1 | survey / R1 |
| 9 | GovTech State Cyber Police UI Theme | Clean white/blue government portal style (Navy `#0b3b60`, Slate `#f8fafc`, accessible contrast) | M2 | survey / R5 |
| 10 | Omnichannel Input Tabs | Streamlit tabs for (1) SMS/Email Text, (2) WhatsApp Image Upload, (3) Live Threat Simulator | M2 | survey / R1 |
| 11 | Sentinel Mode Visual Dashboard | Visual risk cards, confidence gauge, red flags checklist, psychological breakdown, audio player | M2 | survey / R2 |
| 12 | Strike Mode Chat Bubble UI | Interactive multi-turn chat interface using `st.chat_message` and session state for Rahul persona | M2 | survey / R3 / update |
| 13 | State Cyber Police Alert Banner | Prominent alert banner confirming logging to Cyber Police Threat Database on High/Medium threats | M2 | survey / R4 |
| 14 | Graceful API Key Error Handling | Clear UI feedback for missing or invalid Gemini API keys without crashing | M2 | survey / R5 |
| 15 | Verification Script (`verify.py`) | Automated test script verifying backend analysis and threat logging returning PASS/FAIL | M3 | survey / Acceptance |
| 16 | 100% E2E Acceptance & Adversarial Hardening | Comprehensive test suite testing all R1-R5 criteria, negative edge cases, and adversarial validation | M3 | survey / Final |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Core Backend Engine | backend.py, requirements.txt, .venv package installations (Multimodal Gemini, gTTS BytesIO, threat logging, Rahul honeypot, Hinglish dataset loader, mock engine) | none | DONE |
| M2 | GovTech Streamlit Web UI | app.py overhaul: State Cyber Police white/blue styling, Omnichannel tabs, Sentinel dashboard, Strike Mode chat, alert banners, graceful API handling | M1 | IN_PROGRESS |
| M3 | E2E Verification & Hardening | verify.py implementation, automated test suite, 100% E2E pass, adversarial validation | M1, M2 | PLANNED |

## Interface Contracts
### `backend.py` ↔ `app.py` & `verify.py`
```python
def analyze_threat(
    text: Optional[str] = None,
    image: Optional[Union[Image.Image, bytes, str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes input text or image. Returns dictionary:
    {
        "risk_level": "High" | "Medium" | "Low",
        "confidence_score": float (0.0 to 1.0),
        "scam_category": str,
        "red_flags": List[str],
        "psychological_tactics": List[str],
        "extracted_identifiers": {
            "phone_numbers": List[str],
            "upi_ids": List[str],
            "urls": List[str]
        },
        "recommended_action": str,
        "hindi_warning_text": str
    }
    """

def generate_voice_warning(
    threat_data_or_text: Union[Dict[str, Any], str]
) -> io.BytesIO:
    """
    Generates Hindi voice warning audio using gTTS and returns an in-memory BytesIO stream.
    """

def log_threat(
    threat_data: Dict[str, Any],
    file_path: str = "threat_log.csv",
    source_channel: str = "Unknown"
) -> bool:
    """
    Thread-safely logs High/Medium threat identifiers to threat_log.csv.
    Mitigates CSV formula injection. Returns True if logged, False otherwise.
    """

def generate_honeypot_reply(
    message_or_history: Union[str, List[Dict[str, str]]],
    api_key: Optional[str] = None
) -> str:
    """
    Generates a Hinglish time-wasting reply in the Pushpa Devi persona.
    """

def load_sample_threats(
    csv_path: str = "India_Cyber_Scam_Hinglish_Dataset.csv",
    n: int = 5
) -> List[Dict[str, str]]:
    """
    Loads distinct scam examples from the Hinglish dataset.
    Returns list of dicts: [{"category": str, "message": str, "source": str}]
    """
```

## Code Layout
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\requirements.txt`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\app.py`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\verify.py`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\threat_log.csv`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\India_Cyber_Scam_Hinglish_Dataset.csv`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\test_images/`
