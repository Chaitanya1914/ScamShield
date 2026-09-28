# Dispatch — Worker M1 (Core Backend Engine Implementation)

**Working Directory**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m1_1`
**Project Blueprint**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md`
**Original Request**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md`
**Explorer Handoffs**:
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_m1_1\handoff.md`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_m1_2\handoff.md`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_m1_3\handoff.md`

## Write Ownership
You exclusively own:
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\requirements.txt`
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py`
You also have permission to install packages into `.venv` using `.\.venv\Scripts\python.exe -m pip`.

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Tasks
1. Read `ORIGINAL_REQUEST.md` and `PROJECT.md`.
2. Read the three Explorer handoffs and reports for exact implementation code and guidance.
3. Update `requirements.txt`: strictly remove `pytesseract`; ensure `streamlit`, `google-generativeai`, `gTTS`, `Pillow`, `pandas`, `python-dotenv`.
4. Install packages into `.venv` using PowerShell:
   `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
   Verify imports:
   `.\.venv\Scripts\python.exe -c "import streamlit, google.generativeai, gtts, PIL, pandas, dotenv; print('ALL IMPORTS PASS')"`
5. Implement `backend.py` with complete docstrings on all public functions:
   - `analyze_threat(text=None, image=None, api_key=None)`:
     - Accepts raw text or PIL.Image / bytes / UploadedFile directly without OCR (strictly zero pytesseract).
     - Calls Gemini with JSON schema mode if API key is provided.
     - Offline mock fallback pattern matcher if API key is missing or invalid, guaranteeing structured JSON return.
     - Strict return dictionary structure: `risk_level` (High/Medium/Low), `confidence_score` (float), `scam_category`, `red_flags` (list of strings), `psychological_tactics` (list of strings), `extracted_identifiers` (dict with phone_numbers, upi_ids, urls), `recommended_action`, `hindi_warning_text`.
   - `generate_voice_warning(threat_data_or_text)`:
     - Uses `gTTS(text=hindi_text, lang='hi')`.
     - Uses in-memory `io.BytesIO` buffer rewound to position 0 (`seek(0)`). Strictly no temporary disk files.
   - `log_threat(threat_data, file_path="threat_log.csv", source_channel="Unknown")`:
     - Thread-safe using `threading.Lock()`.
     - Neutralizes CSV formula injection (`'`, `=`, `+`, `-`, `@`).
     - Appends High/Medium threats to CSV.
   - `generate_honeypot_reply(message_or_history, api_key=None)`:
     - "Pushpa Devi" 68-year-old grandmother Hinglish persona prompt.
     - Conversational stall tactics, irrelevant questions, fake details, zero PII leaks.
     - Offline mock fallback for test mode.
   - `load_sample_threats(csv_path="India_Cyber_Scam_Hinglish_Dataset.csv", n=5)`:
     - Dynamically samples distinct scam categories from `India_Cyber_Scam_Hinglish_Dataset.csv`.
6. Run unit tests on `backend.py` via `.\.venv\Scripts\python.exe` to verify all functions execute cleanly and return correct types.
7. Deliver your `handoff.md` and report back to parent.

## 2026-09-28T05:21:52Z
<USER_REQUEST>
You are Worker M1 for the ScamShield project.
Your Working Directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m1_1
Project Blueprint: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md
Dispatch Instructions: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m1_1\DISPATCH.md
Original Request: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md

Read your DISPATCH.md and ORIGINAL_REQUEST.md carefully.
Follow the MANDATORY INTEGRITY WARNING verbatim:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Implement requirements.txt (remove pytesseract, add streamlit, google-generativeai, gTTS, Pillow, pandas, python-dotenv), install in .venv, and implement backend.py per the explorer handoffs and PROJECT.md specifications. Run tests with .venv to verify your work. Deliver handoff.md and send a message to parent when done.
</USER_REQUEST>

## 2026-09-28T05:30:38Z
**Context**: Milestone 1 Implementation Guidance
**Content**: Please do not attempt to inspect or list directories outside the project workspace. You have exclusive write ownership of `requirements.txt` and `backend.py`. Proceed directly with:
1. Updating `requirements.txt` in the project root.
2. Running `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` via run_command.
3. Implementing `backend.py` per the explorer specifications.
4. Verifying with `.\.venv\Scripts\python.exe`.
**Action**: Continue with requirements.txt update and backend.py implementation.

## 2026-09-28T05:47:27Z
**Context**: URGENT User Requirement Update for Strike Mode Honeypot
**Content**: The user has officially updated ORIGINAL_REQUEST.md:
"Please update the Strike Mode (Honeypot) persona in the backend code. The user has requested to change the name from 'Pushpa Devi' to 'Rahul' (or 'Rohan'). Please adjust the prompt accordingly (e.g., change the persona from a confused grandmother to a confused average user or college student named Rahul). Ensure this change is reflected in the final backend.py."
**Action**: Please adjust `backend.py` to ensure `generate_honeypot_reply` uses the 'Rahul' persona (confused average user / college student in Hinglish who is naive and asks irrelevant questions).
