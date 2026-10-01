# Survey Explorer 3 — UI Polish & Comprehensive Test Suite
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_3
Parent Orchestrator: 4f70409b-f3dd-4265-ba60-566f458cbcc3
Task: Investigate app.py CSS contrast, .env API key loading, metrics sidebar, Rahul persona, tests/test_suite.py (>=20 tests), requirements.txt, and README.md.

## 2026-10-01T01:45:59Z
You are UI & Testing Explorer (survey instance 3).
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_3
Workspace root: c:\Users\chait\OneDrive\Desktop\Scam Shield
Parent Orchestrator ID: 4f70409b-f3dd-4265-ba60-566f458cbcc3

MANDATORY FIRST STEP: Read c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md, especially section "## 2026-10-01T01:42:44Z".

Your Mission:
Investigate `app.py`, `verify.py`, `requirements.txt`, and requirements for `tests/test_suite.py` and `README.md`.
Analyze:
1. `app.py` UI issues:
   - Identify any CSS contrast bugs (e.g. hardcoded white text on light backgrounds or dark text on dark backgrounds in light/dark mode).
   - Locate and remove the frontend API key input field — ensure API key is loaded exclusively from `.env` via `python-dotenv`.
   - Design the sidebar display for ML model training metrics (accuracy, F1-score, model status).
   - Ensure clear UI indicators when detection is powered by "Local ML Engine (Offline)" vs "Cloud API".
   - Audit all text for the "Rahul" persona — ensure ZERO occurrences of "Pushpa Devi" in user-facing text.
2. Comprehensive Test Suite (`tests/test_suite.py`):
   - Design >=20 test cases validating:
     (a) local ML model cv-accuracy >=90%
     (b) 5 known scam classified High risk & 5 safe classified Low risk
     (c) IoC extraction (phone, UPI, URL) with >=3 test cases each
     (d) threat logging with CSV injection protection
     (e) Hindi voice warning generation
     (f) app launch without import errors
     (g) zero API keys needed to pass all tests
     (h) script prints explicit PASS/FAIL and exits 0 on success, 1 on failure.
3. Documentation and dependencies:
   - What packages are needed in `requirements.txt` (scikit-learn, scipy, joblib, etc.)?
   - What needs to be in `README.md` (architecture diagram, setup, usage)?

Write your comprehensive findings and recommendations to:
`c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_3\handoff.md`
Then use `send_message` to report back to parent `4f70409b-f3dd-4265-ba60-566f458cbcc3`.
