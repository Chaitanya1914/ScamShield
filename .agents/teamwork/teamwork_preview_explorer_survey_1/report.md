# ScamShield — Explorer Survey 1: Environment, Dependencies & Asset Inspection Report

**Date**: 2026-09-28  
**Investigator**: Explorer 1 (`teamwork_preview_explorer_survey_1`)  
**Workspace Root**: `c:\Users\chait\OneDrive\Desktop\Scam Shield`  
**Reference Document**: `.agents/teamwork/ORIGINAL_REQUEST.md`

---

## 1. Executive Summary

This survey provides a comprehensive audit of the execution environment, Python dependencies, virtual environment configuration (`.venv`), existing dataset files, multimodal test assets, and architectural gaps for **ScamShield** — an Omnichannel AI-powered Scam & Fraud Detector web application.

### Key Findings Summary:
1. **Python Runtime & Virtual Environment**: `.venv` contains a healthy 64-bit Python 3.11.9 installation. However, it currently contains only minimal packages (`lxml`, `pip 24.0`, `python-docx`, `setuptools`, `typing_extensions`). None of the project runtime libraries (`streamlit`, `google-generativeai`, `gTTS`, `Pillow`, `pandas`, `python-dotenv`) are installed yet.
2. **Elimination of Tesseract / OCR**: `requirements.txt` currently lists `pytesseract`. Per Requirement R1 and functional acceptance criteria, OCR software (Tesseract) is **strictly disallowed**. Gemini 2.0 / 1.5 Flash natively accepts multimodal inputs (PIL images) directly. `pytesseract` must be removed from `requirements.txt` and the codebase.
3. **Dataset Verification**: `India_Cyber_Scam_Hinglish_Dataset.csv` was verified at 1.34 MB and 10,000 rows across 8 distinct categories (`bank_kyc`, `police_digital_arrest`, `police_blackmail`, `lottery`, `amazon`, `aadhaar`, `relative`, `none`). It provides authentic Hinglish scam messages ideal for the "Simulate Live Threat" feature.
4. **Multimodal Test Assets**: The `test_images/` directory contains 4 pre-rendered PNG screenshots (26 KB - 35 KB) depicting WhatsApp scam conversations (Electricity disconnection threat, KBC lottery, YouTube part-time job, SBI KYC phishing). All are ready for multimodal evaluation.
5. **Windows OS & Audio Engine (gTTS)**: Using in-memory `io.BytesIO` streams rather than disk-based temporary files for `gTTS` completely prevents Windows file-locking `PermissionError` bugs during Streamlit audio playback.
6. **Existing Prototype Gaps**: The existing `app.py` and `backend.py` files are early prototypes that violate core requirements: they rely on Tesseract OCR, use dark cyberpunk styling instead of Government Cyber Police portal styling (white/blue), lack CSV dataset integration in the simulator, and lack the required `verify.py` test harness.

---

## 2. Environment & Virtual Environment (.venv) Audit

### 2.1 Python Environment Details
- **Executable**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.venv\Scripts\python.exe`
- **Version**: Python 3.11.9 (64-bit Windows)
- **Pip Version**: 24.0
- **Existing Installed Packages**:
  ```text
  Package           Version
  ----------------- -------
  lxml              6.1.3
  pip               24.0
  python-docx       1.2.0
  setuptools        65.5.0
  typing_extensions 4.16.0
  ```

### 2.2 Dependency Gap Analysis
| Package | Required For | Status in `.venv` | Recommended Action |
| :--- | :--- | :--- | :--- |
| `streamlit` | Web UI framework, tabs, metrics, chat | **Missing** | Install `>=1.30.0` |
| `google-generativeai` | Gemini 2.0/1.5 API client (text + multimodal) | **Missing** | Install `>=0.8.0` |
| `gTTS` | Google Text-to-Speech Hindi audio alerts | **Missing** | Install `>=2.5.0` |
| `Pillow` | Image loading for multimodal Gemini inputs | **Missing** | Install `>=10.0.0` |
| `pandas` | CSV dataset loading & threat log tabular display | **Missing** | Install `>=2.0.0` |
| `python-dotenv` | Optional environment variable loading | **Missing** | Install `>=1.0.0` |
| `pytesseract` | OCR text extraction | **Present in requirements.txt** | **Remove completely** (Violates R1) |

### 2.3 Proposed Clean `requirements.txt`
```text
streamlit>=1.30.0
google-generativeai>=0.8.0
gTTS>=2.5.0
Pillow>=10.0.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

**Installation Command**:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 3. Dataset Analysis: `India_Cyber_Scam_Hinglish_Dataset.csv`

### 3.1 Dataset Metadata
- **File Path**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\India_Cyber_Scam_Hinglish_Dataset.csv`
- **Size**: 1,343,946 bytes (~1.34 MB)
- **Total Lines**: 10,002 (Header + 10,000 data records + trailing newline)
- **Encoding**: UTF-8

### 3.2 Schema Definition
```text
text,label,scam_category,caller_type,audio_duration,urgency_level,contains_blackmail,language_style
```
| Column | Type | Allowed / Observed Values | Purpose |
| :--- | :--- | :--- | :--- |
| `text` | String | Hinglish conversational / SMS text | Raw suspicious or benign message |
| `label` | String (`'0'` or `'1'`) | `'1'` (Scam), `'0'` (Benign) | Ground truth classification |
| `scam_category` | String | `bank_kyc`, `police_digital_arrest`, `police_blackmail`, `lottery`, `amazon`, `aadhaar`, `relative`, `none` | Threat categorization |
| `caller_type` | String | `bank_scammer`, `police_impersonator`, `other_scammer`, `delivery_agent`, `doctor_clinic`, `family`, `friend`, `office_colleague` | Scammer persona |
| `audio_duration`| Integer | 18 to 260 | Duration in seconds |
| `urgency_level` | String | `high`, `medium`, `low` | Psychological pressure metric |
| `contains_blackmail` | Boolean | `True`, `False` | Extortion indicator |
| `language_style`| String | `hinglish` | Dialect indicator |

### 3.3 Representative Sample Records
1. **Bank KYC Fraud** (`scam_category: bank_kyc`, `label: 1`):
   > *"Ji namaskar Aapka KYC pending hai. Account 2 ghante mein block ho jayega. OTP share kijiye."*
2. **Police Digital Arrest** (`scam_category: police_digital_arrest`, `label: 1`):
   > *"Aap sun rahe hain na? Aapke Aadhaar card ka istemal karke fake SIM issue ki gayi hai."*
3. **Police Blackmail / Extortion** (`scam_category: police_blackmail`, `label: 1`):
   > *"CBI se bol raha hoon. Aapke WhatsApp se ladies ko asleel messages bheje ja rahe hain. Aapko suspect maana ja raha hai."*
4. **Lottery Scam** (`scam_category: lottery`, `label: 1`):
   > *"Inspector Rajesh Kumar bol raha hoon. Congratulations! Aapne ₹40 lakh ka lottery jeeta hai. Processing fee dena hoga."*
5. **Amazon Delivery Fraud** (`scam_category: amazon`, `label: 1`):
   > *"Delhi Police se bol raha hoon. Amazon se bol raha hoon. Aapka parcel hold hai, clearance charge ₹499 dena hoga."*
6. **Legitimate Control Message** (`scam_category: none`, `label: 0`):
   > *"Hello ji Beta ghar aa gaya hoon, darwaza khol do."*

### 3.4 Integration Blueprint for "Simulate Live Threat" (R1)
Currently, `app.py` relies on a hardcoded 6-item Python dictionary. To satisfy R1 and the acceptance criteria:
- Create a loader function in `backend.py`: `get_sample_scams(dataset_path, count=10)`
- Filter rows where `label == '1'` grouped across distinct categories (`police_digital_arrest`, `bank_kyc`, `lottery`, `amazon`, `police_blackmail`, `aadhaar`).
- Include at least 1 benign control message (`label == '0'`).
- Cache the dataset via `@st.cache_data` in Streamlit for near-instant rendering.

---

## 4. Multimodal Test Assets: `test_images/`

### 4.1 Asset Inventory
The `test_images/` directory contains 4 synthetic WhatsApp screenshots generated by `generate_scam_images.py`. All are 800x600 PNG images formatted as WhatsApp chat bubbles on a beige background (`#ECE5DD`):

| File Name | File Size | Core Scam Vector | Embedded Text Snippet | Key Extracted Identifiers |
| :--- | :--- | :--- | :--- | :--- |
| `kbc_lottery_scam.png` | 34,621 B | Lottery / Prize Fraud | *"CONGRATULATIONS!! You have won a lottery of Rs. 25,00,000 from Kaun Banega Crorepati (KBC) & Jio..."* | Phone: `+91 8888888888`<br>Entity: `KBC Head Office Manager Mr. Rana Pratap` |
| `electricity_scam.png` | 28,474 B | Utility Threat / Urgent Disconnection | *"Dear Customer, Your electricity power will be disconnected tonight at 9:30 PM from update office..."* | Phone: `9876543210` |
| `part_time_job_scam.png` | 32,356 B | Part-time Work-from-Home Task Scam | *"Hello, I am a recruiter from Global Tech... Daily salary is Rs. 3000 to Rs. 5000... click this link: http://bit.ly/fake-job-offer"* | URL: `http://bit.ly/fake-job-offer` |
| `hinglish_kyc_scam.png` | 26,574 B | Hinglish Bank KYC / Phishing Link | *"Namaskar, aapka bank account temporarily block kar diya gaya hai KYC pending hone ke karan... click: http://sbi-kyc-update-online.com/"* | URL: `http://sbi-kyc-update-online.com/` |

### 4.2 Acceptance Criteria Alignment
- **Acceptance Criterion**: *"Uploading `test_images/kbc_lottery_scam.png` successfully passes the image to Gemini and returns a valid threat assessment without requiring OCR software."*
- **Multimodal Gemini Implementation**:
  ```python
  from PIL import Image
  import google.generativeai as genai

  def analyze_image_threat(image_file, api_key: str) -> dict:
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel(
          model_name="gemini-2.0-flash",
          system_instruction=SENTINEL_SYSTEM_PROMPT,
          generation_config={"response_mime_type": "application/json"}
      )
      img = Image.open(image_file)
      response = model.generate_content([
          img,
          "Analyze this image message for cyber scam and fraud threats."
      ])
      return json.loads(response.text)
  ```
  This is 100% cloud-based, requires no Tesseract binaries, no Windows system PATH modification, and works across all platforms.

---

## 5. Audio Engine (gTTS) & Windows Compatibility Survey

### 5.1 gTTS Architecture
`gTTS` (Google Text-to-Speech) issues an HTTPS request to `https://translate.google.com/translate_tts` with parameters `ie=UTF-8`, `tl=hi`, `client=tw-ob`.

### 5.2 Windows File-Locking Hazard & Solution
- **The Problem**: In `backend.py` lines 154-156:
  ```python
  tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", prefix="scamshield_warning_")
  tts.save(tmp.name)
  return tmp.name
  ```
  On Windows OS, `NamedTemporaryFile` holds an exclusive file lock until explicitly closed. If Streamlit attempts to read `tmp.name` while still open, or if deletion fails during cleanup, Windows throws `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
- **The Zero-Disk Solution**: Use an in-memory buffer `io.BytesIO`:
  ```python
  import io
  from gtts import gTTS

  def generate_warning_audio_bytes(hindi_text: str) -> bytes:
      """Generate MP3 audio bytes in memory, avoiding Windows file-locking issues."""
      buf = io.BytesIO()
      tts = gTTS(text=hindi_text, lang="hi", slow=False)
      tts.write_to_fp(buf)
      buf.seek(0)
      return buf.getvalue()
  ```
  Streamlit renders this directly:
  ```python
  audio_bytes = generate_warning_audio_bytes(warning_hindi)
  st.audio(audio_bytes, format="audio/mp3", autoplay=True)
  ```
  This guarantees zero Windows file locks, no temporary file leakage, and instant playback.

### 5.3 Offline / Missing Network Resilience
If the environment has restricted network access or the Google Translate endpoint times out:
- Catch exceptions in `generate_warning_audio_bytes`.
- Return `None` gracefully and let the UI display the text warning with a clear fallback indicator.

---

## 6. Threat Logging & GovTech Simulation (`threat_log.csv`)

### 6.1 Requirements
- When High or Medium risk is detected, extract scammer identifiers (`phone_numbers`, `urls`, `upi_ids`, `email_addresses`).
- Append row(s) to `threat_log.csv`.
- Display a prominent alert banner in the UI confirming logging to the "State Cyber Police Threat Database".

### 6.2 Recommended Schema & Implementation
```python
# threat_log.csv format:
# timestamp,risk_level,scam_category,identifier_type,identifier_value
```
- In `backend.py`, ensure that if `threat_log.csv` does not exist, it is created with proper headers.
- If a scam message has High/Medium risk but no specific identifiers (e.g., pure extortion/intimidation), log a row with `identifier_type="General Threat"`, `identifier_value="Content Flagged"` so the incident is always recorded in the GovTech audit trail.

---

## 7. Comparative Gap Analysis: Current Prototype vs. Requirements

| Requirement | Current Prototype (`app.py` / `backend.py`) | Required Target Implementation | Priority |
| :--- | :--- | :--- | :--- |
| **Image Analysis (R1)** | Uses `pytesseract` to OCR text first, then passes text to Gemini | Pass `PIL.Image` directly to Gemini Multimodal API (`gemini-2.0-flash`), **no OCR** | 🚨 Critical |
| **Live Simulator (R1)** | Hardcoded dictionary `SAMPLE_MESSAGES` with 6 static strings | Dynamic loading from `India_Cyber_Scam_Hinglish_Dataset.csv` | 🚨 Critical |
| **UI Aesthetics (R5)** | Dark cyberpunk neon gradient (`#0f0c29` to `#302b63`, glowing text) | State Cyber Police GovTech portal: clean white background (`#ffffff`), navy blue (`#0d47a1` / `#1a365d`), gold accents | 🚨 Critical |
| **Verification Script** | Missing entirely | `verify.py` verifying analyze function JSON schema + `threat_log.csv` append/write | 🚨 Critical |
| **JSON Reliability** | Regex stripping of markdown fences | Gemini structured outputs `generation_config={"response_mime_type": "application/json"}` | High |
| **Audio File Handling** | `NamedTemporaryFile` with Windows lock vulnerability | `io.BytesIO` in-memory streaming to `st.audio` | High |
| **Strike Mode (R3)** | Basic chat messages | Clean chat bubble layout with Pushpa Devi persona in Hinglish | Medium |

---

## 8. Summary of Actionable Recommendations for Implementation

1. **Update `requirements.txt`**:
   Remove `pytesseract`. Keep/add `streamlit`, `google-generativeai`, `gTTS`, `Pillow`, `pandas`, `python-dotenv`.
2. **Install Packages in `.venv`**:
   Execute `pip install -r requirements.txt` into `.venv`.
3. **Refactor `backend.py`**:
   - Add unified multimodal `analyze_threat(content, api_key, is_image=False)`.
   - Update `generate_warning_audio` to use `io.BytesIO`.
   - Add `load_scam_samples(csv_path)` to ingest `India_Cyber_Scam_Hinglish_Dataset.csv`.
   - Ensure `log_threat` handles all threat types cleanly.
4. **Refactor `app.py`**:
   - Implement Government Cyber Police portal theme: clean white background, police navy header, national emblem style, accessible badges.
   - Connect Tab 2 (WhatsApp Screenshot) directly to multimodal analysis.
   - Connect Tab 3 (Simulate Live Threat) to dataset samples.
5. **Create `verify.py`**:
   - Programmatically test backend JSON threat analysis (with mock or live key) and threat logging to `threat_log.csv` printing `PASS`/`FAIL`.
