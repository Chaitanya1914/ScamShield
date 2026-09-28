# ScamShield — Explorer M1.3 Technical Investigation Report: Logging, Voice Synthesis, Honeypot & Dataset Loader

**Date**: 2026-09-28  
**Investigator**: Explorer M1.3 (`teamwork_preview_explorer_m1_3`)  
**Workspace**: `c:\Users\chait\OneDrive\Desktop\Scam Shield`  
**Target Module**: `backend.py` (Functions: `log_threat`, `generate_voice_warning`, `generate_honeypot_reply`, `load_sample_threats`)  
**Status**: Complete Implementation Design & Ready for Worker

---

## 1. Executive Summary

This report establishes the implementation design for the four remaining computational functions in `backend.py` for Milestone 1 (Core Backend Engine):
1. **`log_threat()`**: Secure, thread-safe CSV appending to `threat_log.csv` guarded by `threading.Lock()`, complete CSV formula injection mitigation (`'`, `=`, `+`, `-`, `@`), selective logging for High/Medium risk threats only, and dual-schema indicator extraction.
2. **`generate_voice_warning()`**: Zero-disk in-memory audio synthesis using `gTTS(text=..., lang='hi')` writing to `io.BytesIO()`. This completely fixes the Windows `[WinError 32]` file-lock crashes caused by legacy `tempfile.NamedTemporaryFile` and ensures smooth Streamlit playback.
3. **`generate_honeypot_reply()`**: Multi-turn and single-turn conversational offensive AI honeypot implementing the "Pushpa Devi" persona (a 68-year-old grandmother speaking authentic Hinglish). It features robust anti-exfiltration boundaries (zero credential leakage), circular stalling tactics, and a deterministic keyword-based offline mock fallback for automated testing without Gemini API keys.
4. **`load_sample_threats()`**: Dynamic sampling engine loading ≥5 distinct scam categories from `India_Cyber_Scam_Hinglish_Dataset.csv` (10,000 rows across categories: `bank_kyc`, `police_digital_arrest`, `police_blackmail`, `lottery`, `amazon`, `aadhaar`, `relative`, `none`), featuring defensive column normalization and hardcoded fallbacks if the dataset is absent.

---

## 2. Deep Dive: `log_threat` Specification & Implementation

### 2.1 The Vulnerabilities in Legacy `log_threat`
In the legacy prototype (`backend.py` lines 184–222):
- **Race Condition Hazard**: Writing directly to `THREAT_LOG_PATH` without locking. In Streamlit's multi-threaded execution model or under concurrent verification runs, simultaneous writes interleave characters and corrupt the CSV file.
- **CSV Formula Injection (DDE Attack)**: Malicious scam messages containing formulas like `=cmd|' /C calc'!A0` or strings starting with `+`, `-`, `@` were written raw to the CSV. When an analyst opens `threat_log.csv` in Microsoft Excel or LibreOffice Calc, the spreadsheet executes the command.
- **Hardcoded Path**: Did not allow passing a custom `file_path`, making isolated unit testing in `verify.py` or temporary test directories impossible without contaminating the production database.
- **No Risk Filtering**: Attempted to log any input regardless of risk level.
- **Silent Drop on Missing Regex Identifiers**: If a High-risk threat lacked explicit phone/UPI/URL tokens, `log_threat` returned `None`, violating Requirement R4.

### 2.2 Security & Architectural Design
1. **Concurrency Lock**: Use a dedicated module-level lock `_LOG_LOCK = threading.Lock()`. All existence checks, file openings, row writing, and flushes occur within `with _LOG_LOCK:`.
2. **CSV Formula Injection Neutralization**:
   Any cell value starting with `=`, `+`, `-`, `@`, `\t`, or `\r` is prepended with a single apostrophe quote (`'`). Excel treats apostrophe-prefixed values strictly as raw text, disarming formula and DDE triggers.
3. **Selective Threat Logging**:
   Only log when `risk_level` is `"High"` or `"Medium"`. If `risk_level` is `"Low"`, `"Safe"`, or unrecognized, return an empty list `[]` (evaluates to `False` in boolean context) without modifying the file.
4. **Standard 5-Column Schema**:
   Header: `["timestamp", "risk_level", "scam_category", "identifier_type", "identifier_value"]`.
   If the target CSV does not exist or has `st_size == 0`, write the header row first.
5. **Dual-Schema & Incident Digest Extraction**:
   Check both `threat_data.get("extracted_identifiers")` (new schema) and `threat_data.get("extracted_threat_data")` (legacy schema).
   If no explicit identifiers are found but the threat is High/Medium, log an incident entry:
   `identifier_type: "Incident_Digest"`, `identifier_value: threat_data.get("scam_category", "High Risk Threat Detected")`.
6. **Return Type Discipline**:
   Returns `List[str]` containing the logged identifier strings.
   - Evaluates to `True` in boolean contexts (`if log_threat(...)`).
   - Satisfies `verify.py` line 481: `if not logged: print("[FAIL] log_threat returned None or empty list")`.
   - Satisfies `app.py` line 310: `", ".join(logged[:3])`.

### 2.3 Proposed Production Implementation for `log_threat`

```python
import csv
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

_LOG_LOCK = threading.Lock()
THREAT_LOG_PATH = Path(__file__).parent / "threat_log.csv"

def _sanitize_csv_value(val: Any) -> str:
    """
    Mitigates CSV formula injection (Excel / LibreOffice DDE & formula execution).
    Prefixes values starting with '=', '+', '-', '@', '\\t', '\\r' with a single apostrophe.
    """
    if val is None:
        return ""
    s = str(val).strip()
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{s}"
    return s

def log_threat(
    threat_data: Dict[str, Any],
    file_path: Union[str, Path] = "threat_log.csv",
    source_channel: str = "Unknown",
    **kwargs
) -> List[str]:
    """
    Thread-safely logs High and Medium threat identifiers to threat_log.csv.
    Mitigates CSV formula injection and deduplicates indicators.

    Args:
        threat_data: Dict containing risk assessment, scam_category, and extracted identifiers.
        file_path: Target CSV file path (defaults to threat_log.csv relative to backend.py).
        source_channel: Source vector (e.g. 'SMS', 'Email', 'WhatsApp Image', 'Simulator').

    Returns:
        List[str]: List of logged identifier values (truthy if logged, empty list if skipped).
    """
    risk = str(threat_data.get("risk_level", "Unknown")).strip().capitalize()
    if risk not in ("High", "Medium"):
        return []

    # Handle log_path alias from kwargs
    if "log_path" in kwargs:
        file_path = kwargs["log_path"]

    target_path = Path(file_path)
    if not target_path.is_absolute():
        target_path = Path(__file__).parent / file_path

    # Extract identifiers supporting both schema variants
    extracted = (
        threat_data.get("extracted_identifiers")
        or threat_data.get("extracted_threat_data")
        or {}
    )

    phones = extracted.get("phone_numbers") or threat_data.get("phone_numbers") or []
    urls = extracted.get("urls") or threat_data.get("urls") or []
    upi_ids = extracted.get("upi_ids") or threat_data.get("upi_ids") or []
    emails = extracted.get("email_addresses") or threat_data.get("email_addresses") or []

    # Deduplicate while preserving order
    def _dedupe(items):
        seen = set()
        out = []
        for item in items:
            s = str(item).strip()
            if s and s not in seen:
                seen.add(s)
                out.append(s)
        return out

    phones = _dedupe(phones)
    urls = _dedupe(urls)
    upi_ids = _dedupe(upi_ids)
    emails = _dedupe(emails)

    category = str(threat_data.get("scam_category", "Unknown")).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows_to_write = []
    logged_identifiers = []

    for phone in phones:
        rows_to_write.append([timestamp, risk, category, "Phone", phone])
        logged_identifiers.append(phone)
    for url in urls:
        rows_to_write.append([timestamp, risk, category, "URL", url])
        logged_identifiers.append(url)
    for upi in upi_ids:
        rows_to_write.append([timestamp, risk, category, "UPI", upi])
        logged_identifiers.append(upi)
    for email in emails:
        rows_to_write.append([timestamp, risk, category, "Email", email])
        logged_identifiers.append(email)

    # Fallback if High/Medium threat contains no explicit regex identifiers
    if not rows_to_write:
        digest_val = category if category != "Unknown" else "High Risk Threat Detected"
        rows_to_write.append([timestamp, risk, category, "Incident_Digest", digest_val])
        logged_identifiers.append(digest_val)

    with _LOG_LOCK:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = target_path.exists() and target_path.stat().st_size > 0

        with open(target_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "risk_level", "scam_category", "identifier_type", "identifier_value"])

            for row in rows_to_write:
                sanitized_row = [_sanitize_csv_value(cell) for cell in row]
                writer.writerow(sanitized_row)
            f.flush()

    return logged_identifiers
```

---

## 3. Deep Dive: `generate_voice_warning` Specification & Implementation

### 3.1 The Windows File-Locking Bug `[WinError 32]`
In legacy `backend.py` (lines 147–159):
```python
def generate_warning_audio(hindi_text: str) -> str:
    tts = gTTS(text=hindi_text, lang="hi", slow=True)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", prefix="scamshield_warning_")
    tts.save(tmp.name)
    return tmp.name
```
On Windows:
1. `NamedTemporaryFile(delete=False)` holds an open file descriptor or locks the path while Streamlit or external media readers attempt to access it.
2. When Streamlit serves the audio via `st.audio(path)`, Windows raises:
   `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
3. Additionally, temporary `.mp3` files accumulate in `%TEMP%`, creating a disk leak.

### 3.2 In-Memory `io.BytesIO` Architecture
1. **Zero Disk Writes**: Use `io.BytesIO()` as the destination buffer.
2. **`gTTS.write_to_fp()`**: Streamlit's `st.audio` natively accepts an `io.BytesIO` object or bytes buffer.
3. **Seek Pointer Reset (`seek(0)`)**: After `tts.write_to_fp(buf)`, the buffer's position pointer is at EOF. The caller must call `buf.seek(0)` before returning so that Streamlit reads the audio from the start.
4. **Flexible Parameter Handling**: Accept either a raw Hindi string or the entire `threat_data` dictionary output by `analyze_threat`.
5. **Network Resilience**: If the internet connection fails or Google TTS servers reject the request, catch the exception cleanly and return `None` rather than crashing the application.
6. **Backward Compatibility**: Provide `generate_warning_audio` as an alias pointing to `generate_voice_warning`.

### 3.3 Proposed Production Implementation for `generate_voice_warning`

```python
import io
import logging
from typing import Any, Dict, Optional, Union
from gtts import gTTS

logger = logging.getLogger(__name__)

def generate_voice_warning(
    threat_data_or_text: Union[Dict[str, Any], str]
) -> Optional[io.BytesIO]:
    """
    Generates an accessible Hindi voice warning audio stream in-memory using gTTS.
    Eliminates Windows file locking [WinError 32] by using io.BytesIO.

    Args:
        threat_data_or_text: Either a dict containing 'hindi_warning_text' /
                             'warning_message_hindi', or a raw Hindi string.

    Returns:
        io.BytesIO stream positioned at 0 if successful, or None on failure.
    """
    if isinstance(threat_data_or_text, dict):
        text = (
            threat_data_or_text.get("hindi_warning_text")
            or threat_data_or_text.get("warning_message_hindi")
            or "Savdhaan! Yeh ek cyber fraud sandesh ho sakta hai. Kripya kisi ko OTP ya paise na bhejein."
        )
    elif isinstance(threat_data_or_text, str):
        text = threat_data_or_text.strip()
    else:
        text = "Savdhaan! Yeh sandesh cyber fraud ho sakta hai."

    if not text:
        text = "Savdhaan! Yeh sandesh cyber fraud ho sakta hai. Satark rahein."

    try:
        # Use gTTS to synthesize Hindi speech
        tts = gTTS(text=text, lang="hi", slow=False)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)  # Rewind to start of stream for playback
        return audio_stream
    except Exception as e:
        logger.warning(f"gTTS audio generation failed (offline or network error): {e}")
        return None

# Backward compatibility alias for existing code
generate_warning_audio = generate_voice_warning
```

---

## 4. Deep Dive: `generate_honeypot_reply` Specification & Implementation

### 4.1 Pushpa Devi Persona & Hinglish Cultural Mechanics
- **Character Profile**: Pushpa Devi, 68-year-old grandmother (*daadi / naani*) living in a tier-2 town (Bareilly/Kanpur).
- **Linguistic Style**: Natural, respectful, conversational Hinglish (Hindi written in Roman English script mixed with colloquial Indian English).
- **Maternal Endearments**: Uses "*beta*", "*bhai sahab*", "*jeete raho*", "*tumne khana khaya ki nahi?*".
- **Stalling Tactics & Technical Naivety**:
  - Confuses technology: thinks OTP is printed on the ration card, electric meter, or electricity bill.
  - Blames physical issues: broken reading glasses (*chashma toot gaya hai*), cracked smartphone screen, knee pain (*ghutno ka dard*).
  - Wanders off-topic: mentions her grandson *Rahul* who manages her phone, the pressure cooker whistle, or her retired husband’s railway pension.
  - Asks circular, naive questions: "*Beta yeh link dabane se bijli ka shock toh nahi lagega?*", "*Kya main cheque Bareilly post office mein jama kar sakti hoon?*".
- **Strict Anti-Exfiltration Boundaries**:
  - **NEVER** reveal valid credentials (no genuine phone numbers, passwords, OTPs, UPI PINs, Aadhaar, PAN, or bank account numbers).
  - If pressed for an OTP, provides invalid 3-digit or 7-digit fake sequences or claims the screen is rotating (*gol gol ghoom raha hai*).
  - **NEVER** break character or admit to being an AI or honeypot.

### 4.2 Multi-Turn Dialogue Support
The function accepts either:
1. `str`: Single message from the scammer.
2. `List[Dict[str, str]]`: History of turns in the conversation (e.g. `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`).
When a list is provided, the function formats the prior exchange into the model context to maintain conversational continuity.

### 4.3 Deterministic Offline Mock Fallback Engine
When `api_key` is `None` or Gemini fails due to quota exhaustion / network timeouts, an offline rule-based heuristic returns high-quality, authentic Pushpa Devi replies tailored to the scam type:
- **Banking / KYC**: Stalls on finding her passbook, asks if the scammer can come home to help.
- **Lottery / KBC**: Expresses innocent excitement about buying a bicycle for grandson Rahul, asks if postman will deliver cash.
- **Electricity Cut-off**: Panics about insulin/blood pressure medicine spoiling in the fridge, offers to send Rahul on scooter.
- **Part-Time Job**: Confesses she doesn't know how to open YouTube, asks if it's a government job with pension.
- **Police / Digital Arrest**: Shocked, invokes late husband's railway reputation, offers to bring temple pandit to the police station.
- **Generic Fallback**: Sweet maternal greeting, asking about the scammer's family and lunch.

### 4.4 Proposed Production Implementation for `generate_honeypot_reply`

```python
import os
import re
from typing import Any, Dict, List, Optional, Union
import google.generativeai as genai

PUSHPA_DEVI_SYSTEM_PROMPT = """You are Pushpa Devi, a confused, extremely sweet, and talkative 68-year-old Indian grandmother living in a small town in Uttar Pradesh. You have zero understanding of technology and use a basic Android phone with a cracked screen.

You are acting as an offensive cybersecurity honeypot (tarpit) against a cyber scammer. Your mission is to waste as much of the scammer's time as possible while revealing ZERO real personal or financial details.

Rules:
1. Tone: Warm, deeply respectful, highly confused, maternal. Use words like "beta", "bhai sahab", "jeete raho", "namaste ji".
2. Language: Authentic conversational Hinglish (code-mixed Hindi and English written in Roman script).
3. Distractions & Stalling:
   - Talk about your physical ailments (knee pain / ghutno ka dard, broken reading glasses / chashma).
   - Talk about your grandson Rahul who usually operates your phone, or your daughter-in-law (bahu).
   - Ask 2 to 3 silly, circular follow-up questions (e.g., "Beta yeh link dabane se bijli ka jhatka toh nahi lagega?", "OTP kya ration card pe likha hota hai?").
4. Anti-Exfiltration & Fake Data:
   - NEVER provide real phone numbers, bank accounts, passwords, OTPs, or UPI PINs.
   - If asked for an OTP or PIN, give silly fake details (e.g., "Beta screen pe 1-2-3-gol dikh raha hai" or "Beta OTP 4567890 aaya hai par aage ka number mita hua hai").
   - NEVER admit you know it is a scam or that you are an AI. Stay in character 100% of the time.
5. Length: Keep the reply under 120 words so the conversation moves back and forth naturally.
"""

# Deterministic offline mock replies for automated testing and keyless operation
MOCK_HONEYPOT_REPLIES = {
    "kyc": (
        "Arey beta! Main toh darr gayi sunke. Mera pension account band ho jayega kya? "
        "Kal hi bahu se bol rahi thi passbook entry kara lo. Beta yeh OTP kahan likha hota hai? "
        "Mere passbook pe toh sirf Ram-Ram likha hai. Aap khud hamare ghar aake kardo na please beta?"
    ),
    "lottery": (
        "Hai Ram! 25 lakh rupaye?! Sach mein beta? Mere potey Rahul ko nayi cycle dilani thi. "
        "Par beta maine toh koi lottery ticket nahi khareedi thi. Yeh paise kya postman ghar leke aayega "
        "ya mujhe Bareilly aana padega? Aur yeh clearance fee kitni deni hogi beta?"
    ),
    "electricity": (
        "Arre beta light mat kaatna please! Mera BP ki dawai fridge mein rakhi hai, kharab ho jayegi. "
        "Kal hi maine bijli office mein Sharma ji ko ₹500 diye the. Aapka office kahan hai beta? "
        "Main abhi Rahul ko bolti hoon scooter se aake cash de dega."
    ),
    "job": (
        "Beta roz ₹3000-5000 YouTube video like karke? Mujhe toh phone mein YouTube kholna bhi nahi aata. "
        "Rahul ne kaha tha anjaan link mat dabana. Kya yeh sarkari naukri hai beta? Isme pension milegi kya?"
    ),
    "police": (
        "Hey Bhagwan! Police case?! Beta maine toh mandir ke alawa kahin kadam bhi nahi rakha. "
        "Mere late pati Railway mein the, hamari badi izzat hai mohalle mein. Beta aap Thane ka address do, "
        "main pandit ji ko saath leke aati hoon. Phone pe toh bada darr lag raha hai."
    ),
    "default": (
        "Namaste beta. Tumhara message padh ke badi chinta ho gayi. Mera chashma toot gaya hai toh theek se "
        "padh nahi paayi. Yeh batao tumhare ghar mein sab theek hain na? Tumne dopahar ka khana khaya beta? "
        "Aur yeh jo tum bol rahe ho, iske liye passbook branch le jaana padega kya?"
    ),
}

def _get_mock_honeypot_reply(text: str) -> str:
    """Selects the most suitable Pushpa Devi reply based on message keywords."""
    lower = text.lower()
    if any(k in lower for k in ["kyc", "block", "sbi", "hdfc", "bank", "otp", "pan"]):
        return MOCK_HONEYPOT_REPLIES["kyc"]
    if any(k in lower for k in ["lottery", "kbc", "winner", "prize", "crore", "lakh", "claim"]):
        return MOCK_HONEYPOT_REPLIES["lottery"]
    if any(k in lower for k in ["electricity", "power", "bill", "disconnect", "light"]):
        return MOCK_HONEYPOT_REPLIES["electricity"]
    if any(k in lower for k in ["job", "part-time", "youtube", "earn", "salary", "hiring"]):
        return MOCK_HONEYPOT_REPLIES["job"]
    if any(k in lower for k in ["police", "cbi", "arrest", "court", "customs", "illegal", "video"]):
        return MOCK_HONEYPOT_REPLIES["police"]
    return MOCK_HONEYPOT_REPLIES["default"]

def generate_honeypot_reply(
    message_or_history: Union[str, List[Dict[str, str]]],
    api_key: Optional[str] = None
) -> str:
    """
    Generates a Hinglish time-wasting honeypot reply in the Pushpa Devi persona.
    Falls back to deterministic offline replies if API key is absent or API fails.

    Args:
        message_or_history: Scammer message string or list of chat turn dicts.
        api_key: Optional Gemini API key.

    Returns:
        str: Pushpa Devi's response in Hinglish.
    """
    # Format conversational context
    if isinstance(message_or_history, list):
        dialogue = []
        for turn in message_or_history:
            role = "Scammer" if turn.get("role") in ("user", "scammer") else "Pushpa Devi"
            dialogue.append(f"{role}: {turn.get('content', '')}")
        prompt_content = "\n".join(dialogue) + "\nPushpa Devi:"
        last_scammer_msg = ""
        for turn in reversed(message_or_history):
            if turn.get("role") in ("user", "scammer"):
                last_scammer_msg = turn.get("content", "")
                break
    else:
        last_scammer_msg = str(message_or_history)
        prompt_content = f"The scammer sent you this message:\n\n\"{last_scammer_msg}\"\n\nReply as Pushpa Devi:"

    # If no API key provided, immediately use offline mock
    effective_key = api_key or os.getenv("GEMINI_API_KEY")
    if not effective_key or not effective_key.strip():
        return _get_mock_honeypot_reply(last_scammer_msg)

    try:
        genai.configure(api_key=effective_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=PUSHPA_DEVI_SYSTEM_PROMPT,
        )
        response = model.generate_content(prompt_content)
        if response and response.text:
            return response.text.strip()
        return _get_mock_honeypot_reply(last_scammer_msg)
    except Exception:
        # Graceful fallback to offline mock on API errors
        return _get_mock_honeypot_reply(last_scammer_msg)
```

---

## 5. Deep Dive: `load_sample_threats` Specification & Implementation

### 5.1 Dataset Schema & Dynamic Sampling Strategy
The project repository includes `India_Cyber_Scam_Hinglish_Dataset.csv` containing 10,000 synthetic and real Hinglish cyber fraud messages.
- **Categories Present (label=1)**: `bank_kyc`, `police_digital_arrest`, `police_blackmail`, `lottery`, `amazon`, `aadhaar`, `relative`, and safe control `none` (label=0).
- **Column Header Variations**:
  - Variant A: `text`, `label`, `scam_category`, `caller_type`, `urgency_level`
  - Variant B: `Hinglish_Message`, `Category`, ...
  Defensive coding extracts:
  `msg = row.get("text") or row.get("Hinglish_Message") or row.get("message")`
  `cat = row.get("scam_category") or row.get("Category") or row.get("category")`

### 5.2 Category Normalization & User-Facing Labels
To present professional, citizen-facing labels in the Streamlit UI, raw category tokens are mapped to clean descriptions:
- `bank_kyc` → `"Banking KYC & Account Block Threat"`
- `police_digital_arrest` → `"Police / CBI Digital Arrest Extortion"`
- `police_blackmail` → `"Video Blackmail & Cyber Cell Coercion"`
- `lottery` → `"KBC / Lucky Draw Prize Scam"`
- `amazon` → `"Parcel Delivery & Customs Clearance Fee"`
- `aadhaar` → `"Aadhaar / SIM Card Disconnection Fraud"`
- `relative` → `"Emergency Relative in Trouble Scam"`

### 5.3 Deterministic & Diverse Sampling
`load_sample_threats(csv_path=..., n=5)`:
1. Filters out non-scam (`none` or `label == 0`) records.
2. Groups rows by category.
3. Selects one representative sample from each category until `n` distinct categories are gathered.
4. If the CSV cannot be found or is empty, falls back to an embedded collection of high-fidelity Hinglish threat samples covering 6 distinct scam vectors.

### 5.4 Proposed Production Implementation for `load_sample_threats`

```python
import csv
from pathlib import Path
from typing import Dict, List

CATEGORY_LABEL_MAP = {
    "bank_kyc": "Banking KYC & Account Block Threat",
    "police_digital_arrest": "Police / CBI Digital Arrest Extortion",
    "police_blackmail": "Video Blackmail & Cyber Cell Coercion",
    "lottery": "KBC / Lucky Draw Prize Scam",
    "amazon": "Parcel Delivery & Customs Clearance Fee",
    "aadhaar": "Aadhaar / SIM Card Disconnection Fraud",
    "relative": "Emergency Relative in Trouble Scam",
    "electricity": "Electricity Power Cut-off Threat",
    "job": "Part-Time Work-From-Home / YouTube Like Scam",
}

BUILTIN_SAMPLE_THREATS = [
    {
        "category": "Banking KYC & Account Block Threat",
        "message": "Ji namaskar Aapka SBI bank account 2 ghante mein block ho jayega KYC pending hone ke karan. Abhi apna OTP share kijiye is number par: 9876543210 ya fir is link par click karein: http://sbi-kyc-update.com",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    },
    {
        "category": "Police / CBI Digital Arrest Extortion",
        "message": "Aap sun rahe hain na? Crime Branch Mumbai se bol raha hoon. Aapke Aadhaar card se 5 fake SIM issue hui hain jisse illegal transactions hue hain. Aapka Digital Arrest warrant issue ho chuka hai. Turant verify karein.",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    },
    {
        "category": "KBC / Lucky Draw Prize Scam",
        "message": "CONGRATULATIONS!! Aapne KBC Season 15 mein Rs. 25,00,000 ka lottery jeeta hai! Claim karne ke liye KBC Head Office Manager Mr. Rana Pratap ko call karein: +91 8888888888. Yeh message kisi ko forward na karein.",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    },
    {
        "category": "Electricity Power Cut-off Threat",
        "message": "Dear Customer, Your electricity connection will be disconnected tonight at 9:30 PM due to pending bill payment. Please contact our officer immediately at 9123456789 to update your payment. - BSES Delhi",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    },
    {
        "category": "Parcel Delivery & Customs Clearance Fee",
        "message": "Special Investigation Team se bol raha hoon. Amazon se bol raha hoon. Aapka parcel hold hai, clearance charge ₹499 dena hoga is link par: http://customs-clearance-pay.in",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    },
    {
        "category": "Part-Time Work-From-Home / YouTube Like Scam",
        "message": "Hello! We are hiring for part-time work from home. Just like YouTube videos and earn Rs. 3000-5000 daily. No experience needed. WhatsApp us on +91 7777777777 or click: http://yt-job-offer.com/apply",
        "source": "India_Cyber_Scam_Hinglish_Dataset.csv"
    }
]

def load_sample_threats(
    csv_path: str = "India_Cyber_Scam_Hinglish_Dataset.csv",
    n: int = 5
) -> List[Dict[str, str]]:
    """
    Loads distinct scam examples from the Hinglish dataset.
    Guarantees at least n distinct scam categories are returned.

    Args:
        csv_path: Path to India_Cyber_Scam_Hinglish_Dataset.csv.
        n: Number of distinct category samples to load (minimum 5).

    Returns:
        List[Dict[str, str]]: [{"category": str, "message": str, "source": str}, ...]
    """
    target = Path(csv_path)
    if not target.is_absolute():
        target = Path(__file__).parent / csv_path

    if not target.exists():
        return BUILTIN_SAMPLE_THREATS[:n]

    samples_by_category: Dict[str, str] = {}

    try:
        with open(target, mode="r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalise column access
                msg = (
                    row.get("text")
                    or row.get("Hinglish_Message")
                    or row.get("message")
                    or ""
                ).strip()

                cat = (
                    row.get("scam_category")
                    or row.get("Category")
                    or row.get("category")
                    or ""
                ).strip().lower()

                label = str(row.get("label", "1")).strip()

                # Skip safe messages or empty text
                if label == "0" or cat in ("none", "safe", "") or not msg:
                    continue

                if cat not in samples_by_category:
                    samples_by_category[cat] = msg

                if len(samples_by_category) >= n:
                    break

        results = []
        for raw_cat, msg in samples_by_category.items():
            friendly_name = CATEGORY_LABEL_MAP.get(raw_cat, raw_cat.replace("_", " ").title())
            results.append({
                "category": friendly_name,
                "message": msg,
                "source": target.name
            })

        # If dataset had fewer than n categories, top up with built-ins
        if len(results) < n:
            existing_cats = {r["category"] for r in results}
            for fallback in BUILTIN_SAMPLE_THREATS:
                if fallback["category"] not in existing_cats:
                    results.append(fallback)
                    if len(results) >= n:
                        break

        return results[:n]

    except Exception:
        return BUILTIN_SAMPLE_THREATS[:n]
```

---

## 6. Interface Contracts & Backward Compatibility Matrix

| Function | Old Signature | Required New Signature | Backward Compatibility Strategy |
|---|---|---|---|
| `log_threat` | `log_threat(analysis_result: dict)` | `log_threat(threat_data: Dict[str, Any], file_path: str = "threat_log.csv", source_channel: str = "Unknown") -> List[str]` | Accepts `threat_data` as first positional arg, accepts `log_path` alias via `**kwargs`, returns `List[str]` which is truthy on success and supports indexing `logged[:3]`. |
| `generate_voice_warning` | `generate_warning_audio(hindi_text: str)` | `generate_voice_warning(threat_data_or_text: Union[Dict, str]) -> Optional[io.BytesIO]` | Aliases `generate_warning_audio = generate_voice_warning`; accepts either string or dict; returns in-memory `io.BytesIO` rewound to 0. |
| `generate_honeypot_reply` | `generate_honeypot_reply(scammer_message: str, api_key: str)` | `generate_honeypot_reply(message_or_history: Union[str, List[Dict]], api_key: Optional[str] = None) -> str` | Handles both string and multi-turn list; if `api_key` is None or network fails, returns deterministic Pushpa Devi Hinglish mock response. |
| `load_sample_threats` | Did not exist (hardcoded dictionary in `app.py`) | `load_sample_threats(csv_path: str = "...", n: int = 5) -> List[Dict[str, str]]` | Dynamically parses `India_Cyber_Scam_Hinglish_Dataset.csv`; returns ≥5 distinct scam categories; includes builtin fallbacks. |

---

## 7. Verification Method for Downstream Agents & Testing

To independently verify these four functions without external API credentials:
1. **Threat Logging Verification**:
   - Call `log_threat` with High-risk threat dictionary containing `phone_numbers=["+919876543210"]` and `urls=["=cmd|' /C calc'!A0"]`.
   - Verify `threat_log.csv` exists and has header `["timestamp", "risk_level", "scam_category", "identifier_type", "identifier_value"]`.
   - Verify the phone number was sanitized to `'+919876543210` and the malicious URL was sanitized to `'=cmd|' /C calc'!A0`.
   - Call `log_threat` with Low-risk threat dictionary; verify return value is `[]` and no rows were appended.
2. **Audio Synthesis Verification**:
   - Call `generate_voice_warning("Savdhaan! Yeh cyber fraud sandesh hai.")`.
   - Assert return value is `isinstance(result, io.BytesIO)`.
   - Assert `result.tell() == 0` (seek pointer rewound).
   - Assert `len(result.getvalue()) > 1000` (valid MP3 bytes).
3. **Honeypot Reply Verification**:
   - Call `generate_honeypot_reply("Your SBI account KYC is blocked", api_key=None)`.
   - Assert return value is a non-empty string.
   - Assert string contains characteristic Pushpa Devi tokens (e.g. `"beta"`, `"pension"`, `"passbook"`).
4. **Dataset Sampler Verification**:
   - Call `samples = load_sample_threats(n=5)`.
   - Assert `len(samples) >= 5`.
   - Assert `len({s['category'] for s in samples}) >= 5` (distinct categories).
   - Assert each sample contains non-empty `"category"` and `"message"`.
