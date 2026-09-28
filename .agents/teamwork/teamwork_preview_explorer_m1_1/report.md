# Milestone 1.1 Dependency & Packaging Strategy Report

**Project**: ScamShield  
**Component**: Core Environment & Dependency Cleanliness  
**Target Environment**: Python 3.11.9 (`.venv`) on Windows (PowerShell)  
**Author**: Explorer M1.1  
**Date**: 2026-09-28  

---

## 1. Executive Summary

This investigation establishes the definitive Python packaging and virtual environment installation strategy for Milestone 1 of the ScamShield application. 

Key Findings:
1. **`requirements.txt` must be cleaned**: Remove `pytesseract` (which introduces external C++ binary dependencies and violates the zero-OCR Gemini multimodal requirement) and add `pandas` (required for sampling the 10,000-row Hinglish scam dataset).
2. **Virtual environment already initialized**: A clean Python 3.11.9 virtual environment is located at `c:\Users\chait\OneDrive\Desktop\Scam Shield\.venv` with `include-system-site-packages = false`.
3. **Targeted pip execution**: All package installations must strictly invoke `.\.venv\Scripts\python.exe -m pip` to prevent contamination of the global Python environment.
4. **Zero-OCR Multimodal Architecture**: Codebase inspection revealed existing OCR hooks in `backend.py` (lines 18–27, 81–94) and `app.py` (lines 13, 200–201) that must be refactored by the M1 and M2 workers to pass `PIL.Image` objects directly to Gemini 1.5/2.0 Flash.

---

## 2. Environment Audit

### 2.1 Virtual Environment Inspection
- **Path**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.venv`
- **Configuration** (`.venv\pyvenv.cfg`):
  ```ini
  home = C:\Users\chait\AppData\Local\Programs\Python\Python311
  include-system-site-packages = false
  version = 3.11.9
  executable = C:\Users\chait\AppData\Local\Programs\Python\Python311\python.exe
  command = C:\Users\chait\AppData\Local\Programs\Python\Python311\python.exe -m venv C:\Users\chait\OneDrive\Desktop\Scam Shield\.venv
  ```
- **Current `site-packages` Content**:
  - `pip` (v24.0)
  - `setuptools` (v65.5.0)
  - `typing_extensions` (v4.16.0)
  - `python-docx` (v1.2.0)
  - `lxml` (v6.1.3)
  - *Note*: `streamlit`, `google-generativeai`, `gTTS`, `Pillow`, `pandas`, `python-dotenv`, and `pytesseract` are currently **not installed** in `.venv`.

### 2.2 Codebase OCR Audit
A full pattern search across the workspace for `tesseract` / `pytesseract` identified the following touchpoints:
- `requirements.txt`: Line 5 references `pytesseract`.
- `backend.py`: 
  - Lines 20–27: Conditional import of `pytesseract` and hardcoded path check `C:\Program Files\Tesseract-OCR\tesseract.exe`.
  - Lines 81–94: `extract_text_from_image(image_file)` which uses `pytesseract.image_to_string()`.
- `app.py`:
  - Line 13: Import of `TESSERACT_AVAILABLE`.
  - Lines 200–201: Warning prompt advising users to download Tesseract binaries from GitHub.
- `ORIGINAL_REQUEST.md`: Explicitly dictates requirement R1:
  > *"passes the image directly to the Gemini API (multimodal processing, NO Tesseract)"*

---

## 3. Clean `requirements.txt` Specification

The updated `requirements.txt` strictly retains the 6 core application packages with compatible version constraints for Python 3.11.9 on Windows:

```txt
streamlit>=1.32.0,<2.0.0
google-generativeai>=0.8.0
gTTS>=2.5.0
Pillow>=10.2.0
pandas>=2.2.0
python-dotenv>=1.0.0
```

### Package Rationale & Compatibility Matrix

| Package | Minimum Version | Primary Role in ScamShield | Compatibility Rationale |
|---|---|---|---|
| `streamlit` | `>=1.32.0,<2.0.0` | Frontend web UI (`app.py`), Omnichannel tabs, chat-bubble interface (`st.chat_message`), audio playback | Modern Streamlit APIs provide native chat components and stable audio rendering without breaking changes. |
| `google-generativeai` | `>=0.8.0` | Core LLM engine (`backend.py`), multimodal vision analysis, structured JSON schema response | Natively accepts `PIL.Image` objects and text in `generate_content([image, prompt])`, removing any need for OCR binaries. Supports `gemini-2.0-flash` and `gemini-1.5-flash`. |
| `gTTS` | `>=2.5.0` | Sentinel Voice Warning (`backend.py`) Hindi audio generation | Python 3.11 compatible; supports writing directly to an in-memory `io.BytesIO` buffer via `tts.write_to_fp()`, avoiding Windows file locking issues. |
| `Pillow` | `>=10.2.0` | Screenshot image handling, format conversion, and inspection | Standard imaging library with pre-built binary wheels for Windows x86_64 and Python 3.11.9. |
| `pandas` | `>=2.2.0` | Hinglish dataset ingestion (`India_Cyber_Scam_Hinglish_Dataset.csv`) | High-performance CSV parsing and multi-category stratified sampling for the Threat Simulator. |
| `python-dotenv` | `>=1.0.0` | Environment configuration | Automatically loads `GEMINI_API_KEY` from a local `.env` file during local development/testing. |

### Exclusion of `pytesseract`
- **No external binaries**: Eliminating `pytesseract` removes the prerequisite for Windows users to download and install a separate ~50MB C++ installer (`tesseract.exe`).
- **Superior accuracy**: Gemini 1.5/2.0 multimodal vision natively understands WhatsApp typography, emojis, background colors, contact headers, and Hinglish slang with greater fidelity than classic Tesseract OCR.
- **Architectural alignment**: Satisfies Requirement R1 and Milestone 1 deliverables.

---

## 4. Exact Installation Commands for the Worker

The implementing Worker should execute the following commands in the workspace root (`c:\Users\chait\OneDrive\Desktop\Scam Shield`) within PowerShell.

### Step 1: Write Updated `requirements.txt`
Update `requirements.txt` to contain:
```
streamlit>=1.32.0,<2.0.0
google-generativeai>=0.8.0
gTTS>=2.5.0
Pillow>=10.2.0
pandas>=2.2.0
python-dotenv>=1.0.0
```

### Step 2: Ensure `pytesseract` is Uninstalled
Run in PowerShell:
```powershell
.\.venv\Scripts\python.exe -m pip uninstall -y pytesseract
```

### Step 3: Install Required Dependencies into `.venv`
Run in PowerShell:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
*Note: Using `.\.venv\Scripts\python.exe -m pip` guarantees that only `.venv` is modified and the global Python environment remains completely untouched.*

---

## 5. Verification Commands for the Worker

The implementing Worker must run the following verification steps to validate the installation.

### 5.1 Verification Test 1: Verify All Required Package Imports
Run in PowerShell:
```powershell
.\.venv\Scripts\python.exe -c "import streamlit, google.generativeai, gtts, PIL, pandas, dotenv; print('PASS: All required packages successfully imported into .venv!')"
```

### 5.2 Verification Test 2: Print Package Versions
Run in PowerShell:
```powershell
.\.venv\Scripts\python.exe -c "import streamlit as st, google.generativeai as genai, gtts, PIL, pandas as pd, dotenv; print(f'streamlit: {st.__version__}\ngoogle-generativeai: {genai.__version__}\ngTTS: {gtts.__version__}\nPillow: {PIL.__version__}\npandas: {pd.__version__}\npython-dotenv: {dotenv.__version__}')"
```

### 5.3 Verification Test 3: Confirm `pytesseract` is Absent
Run in PowerShell:
```powershell
.\.venv\Scripts\python.exe -c "try: import pytesseract; print('FAIL: pytesseract is still installed'); exit(1) except ImportError: print('PASS: pytesseract is NOT installed (Clean)')"
```

### 5.4 Verification Test 4: Verify In-Memory Audio Synthesis
To ensure `gTTS` works in-memory without Windows file locking:
```powershell
.\.venv\Scripts\python.exe -c "import io; from gtts import gTTS; fp = io.BytesIO(); tts = gTTS(text='Satark rahein', lang='hi'); tts.write_to_fp(fp); fp.seek(0); assert len(fp.read()) > 0; print('PASS: In-memory gTTS audio synthesis verified!')"
```

---

## 6. Recommendations for Downstream M1 Implementation

When Milestone 1 Worker implements `backend.py`:
1. **Multimodal API Call**:
   Accept `image` as `Union[PIL.Image.Image, bytes, str, None]`. When present, pass the PIL image directly in `model.generate_content([image, prompt])`.
2. **In-Memory Audio**:
   Refactor `generate_warning_audio()` to `generate_voice_warning()` returning `io.BytesIO` instead of temporary files on disk.
3. **Dataset Ingestion**:
   Implement `load_sample_threats(csv_path, n=5)` using `pandas.read_csv()` to group by `scam_category` and sample representative examples.
