# Handoff Report — Explorer Survey 2 (Backend, Multimodal Gemini & Threat Logging)

## 1. Observation
1. **Existing Multimodal Implementation Flaw**:
   - In `backend.py` (lines 18–28, 79–94), image processing is implemented via `pytesseract`:
     ```python
     def extract_text_from_image(image_file) -> str:
         if not TESSERACT_AVAILABLE:
             return "[OCR Error] Tesseract is not installed. Please install Tesseract-OCR to use image scanning."
         ...
         text = pytesseract.image_to_string(img, lang="eng+hin")
     ```
   - In `requirements.txt` (line 5), `pytesseract` is listed as a dependency.
   - In `ORIGINAL_REQUEST.md` (lines 21–22, 41):
     `"passes the image directly to the Gemini API (multimodal processing, NO Tesseract)"`
     `"Uploading test_images/kbc_lottery_scam.png successfully passes the image to Gemini and returns a valid threat assessment without requiring OCR software"`

2. **Environment & Dependency Status**:
   - `pip list` in `.venv\Scripts\python.exe` showed:
     `lxml 6.1.3, pip 24.0, python-docx 1.2.0, setuptools 65.5.0, typing_extensions 4.16.0`.
     Neither `streamlit`, `google-generativeai`, `gTTS`, `pillow`, nor `pandas` are installed in `.venv` yet.
   - System Python (`python`) has `google-generativeai 0.8.6`, `gTTS 2.5.4`, `pillow 12.2.0`, `streamlit 1.55.0`, `pandas 3.0.2`, `python-dotenv 1.2.2`.

3. **Audio Generation Issue**:
   - In `backend.py` (lines 147–159):
     ```python
     def generate_warning_audio(hindi_text: str) -> str:
         tts = gTTS(text=hindi_text, lang="hi", slow=True)
         tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", prefix="scamshield_warning_")
         tts.save(tmp.name)
         return tmp.name
     ```
   - On Windows, `NamedTemporaryFile(delete=False)` creates file lock collisions (`[WinError 32]`) when accessed by Streamlit/browser, and leaks temporary files indefinitely on disk.
   - Streamlit `st.audio()` accepts raw `bytes` or `io.BytesIO` buffers directly without writing to disk.

4. **Threat Logging Status**:
   - In `backend.py` (lines 185–221):
     `log_threat` writes directly to `THREAT_LOG_PATH` without thread locking (`_LOG_LOCK`), lacks sanitization against CSV formula injection (`=`, `@`, `+`, `-`), does not parameterize `log_path` for isolated testing, and duplicates phone/URL entries if repeated.

5. **Dataset Simulation & Test Assets**:
   - `India_Cyber_Scam_Hinglish_Dataset.csv` exists in the workspace root with 10,002 rows and columns: `text, label, scam_category, caller_type, audio_duration, urgency_level, contains_blackmail, language_style`.
   - `app.py` currently hardcodes a dictionary `SAMPLE_MESSAGES` of 6 messages instead of loading from `India_Cyber_Scam_Hinglish_Dataset.csv`.
   - `test_images/` contains 4 synthetic scam screenshots: `electricity_scam.png`, `hinglish_kyc_scam.png`, `kbc_lottery_scam.png`, `part_time_job_scam.png`.

6. **Automated Verification Script**:
   - No `verify.py` exists yet in the workspace root.
   - `ORIGINAL_REQUEST.md` (lines 62–64) requires a standalone script `verify.py` that tests backend JSON analysis and `threat_log.csv` creation with `PASS`/`FAIL` output.

---

## 2. Logic Chain
1. *From Observation 1*: The requirement specifically mandates multimodal processing without Tesseract. Because `google-generativeai` models (`gemini-2.0-flash` and `gemini-1.5-flash`) natively accept `PIL.Image.Image` objects and image byte streams, `pytesseract` can and should be completely removed from `backend.py` and `requirements.txt`.
2. *From Observation 2*: Because `.venv` currently lacks the required packages, all dependencies must be installed into `.venv` before running Streamlit or `verify.py`.
3. *From Observation 3*: Because Windows file locking causes `PermissionError` when deleting or modifying open temporary files, and because Streamlit `st.audio` supports in-memory bytes, refactoring `generate_warning_audio` to return `io.BytesIO().getvalue()` (bytes) completely eliminates disk leaks and file locking issues.
4. *From Observation 4*: Because Streamlit is multi-threaded and `verify.py` needs to test threat logging without altering the production database, `log_threat` must use a `threading.Lock()`, accept an optional `log_path` parameter, sanitize against CSV formula injection, and deduplicate extracted identifiers.
5. *From Observation 5*: To fulfill Acceptance Criterion R1 ("loads at least 5 distinct scam examples from the Hinglish CSV dataset"), `backend.py` should provide a helper `load_sample_threats()` that dynamically parses rows with `label == 1` across distinct categories from `India_Cyber_Scam_Hinglish_Dataset.csv`.
6. *From Observation 6*: To allow `verify.py` to succeed deterministically in automated environments without requiring a live paid Gemini API key, `analyze_threat` must include an offline heuristic fallback mode that recognizes scam patterns (KBC, KYC, electricity, digital arrest) and returns structured JSON with extracted IOCs.

---

## 3. Caveats
- `gTTS` requires outbound internet access to reach Google's Translate TTS API (`translate.google.com`). If running in an air-gapped network, voice generation will catch the exception and return `None`, falling back to visual text alerts.
- Live Gemini API calls require a valid `GEMINI_API_KEY` provided by the user in the Streamlit UI or set in the environment. Offline heuristic fallback covers tests, but live deployment requires user input.
- No other areas uninvestigated.

---

## 4. Conclusion
1. **Multimodal Gemini**: Refactor `backend.py`'s `analyze_threat` to accept `content: Union[str, Image.Image, io.BytesIO]`. Delete `pytesseract` and all Tesseract OCR code. Set `generation_config={"response_mime_type": "application/json"}` to guarantee clean JSON without markdown code blocks.
2. **Accessible Voice Warning**: Refactor `generate_warning_audio` to return in-memory `bytes` via `io.BytesIO()`. Enforce Devanagari Hindi in the Sentinel prompt for clear pronunciation.
3. **GovTech Logging**: Upgrade `log_threat` with `_LOG_LOCK = threading.Lock()`, `log_path` parameterization, CSV injection prefixing (`'`), and deduplication.
4. **Offline Mock Fallback**: Add heuristic pattern-matching to `analyze_threat` when `mock=True` or `api_key == "MOCK_KEY"` or `SCAMSHIELD_MOCK_MODE == "1"` so `verify.py` passes 100% reliably.
5. **Dataset Ingestion**: Implement `load_sample_threats()` in `backend.py` to feed `app.py` from `India_Cyber_Scam_Hinglish_Dataset.csv`.

---

## 5. Verification Method
1. **Multimodal Inspection**:
   - Inspect `backend.py`: Verify no `import pytesseract` or `tesseract_cmd` references exist.
   - Verify `analyze_threat` accepts PIL Image or bytes and passes directly to `model.generate_content([prompt, img])`.
2. **Audio Bytes Verification**:
   - Verify `generate_warning_audio` returns `bytes` or `None`, not a temporary file path string.
3. **Threat Logging Verification**:
   - Run a test script writing to a custom test CSV path; verify header row exists, rows contain `[timestamp, risk_level, scam_category, identifier_type, identifier_value]`, and no formula execution vulnerabilities exist.
4. **Automated Verification Command**:
   - Once implemented by the team, run `.\.venv\Scripts\python.exe verify.py` or `python verify.py` from the project root; verify it outputs `PASS` and exits with code 0.
