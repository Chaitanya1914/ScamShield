## 2026-10-01T04:25:34Z
You are Worker M2 (Professional Streamlit UI Polish).
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m2_v2
Workspace root: c:\Users\chait\OneDrive\Desktop\Scam Shield
Parent Orchestrator ID: 4f70409b-f3dd-4265-ba60-566f458cbcc3

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY FIRST STEP: Read:
1. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md (especially section "## 2026-10-01T01:42:44Z")
2. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md
3. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_3\handoff.md

Your Exclusive File Write Boundaries: `app.py`, `.streamlit/config.toml`. Do NOT edit backend.py, scam_detector.py, or tests.

Your Mission:
1. Create `.streamlit/config.toml` enforcing the GovTech high-contrast theme:
   ```toml
   [theme]
   primaryColor = "#0b3b60"
   backgroundColor = "#f8fafc"
   secondaryBackgroundColor = "#ffffff"
   textColor = "#0f172a"
   font = "sans serif"
   ```
2. In `app.py`:
   - Fix ALL CSS contrast and readability bugs in light and dark mode. Review Explorer 3's handoff for exact CSS fixes:
     - Sidebar container `section[data-testid="stSidebar"]` must have explicit dark text `#0f172a`.
     - Card containers (`.gov-card`, `.threat-card-*`, `.ncrp-dispatch-banner`, `.hindi-audio-card`, `.stMetric`) must have explicit dark text `#0f172a` and clean borders/backgrounds so text is 100% readable in all themes.
   - HIDE & SECURE API KEY:
     - Remove ANY API key input field from the frontend UI.
     - Load `GEMINI_API_KEY` exclusively from `.env` via `python-dotenv`.
     - In the sidebar, display Cloud API status as "Optional Secondary Layer" (Active if key configured in `.env`, Standby if missing).
   - Sidebar ML Model Metrics Card:
     - In the sidebar, display a prominent card showing real ML model metrics: Status (Active / On-Device Primary), Cross-Validated Accuracy (e.g. 99.2%), F1-Score (e.g. 0.992), Dataset Size (10,000 Hinglish messages). Fetch metrics dynamically via `backend.get_model_metrics()` or `scam_detector.detector.get_metrics()`.
   - Detection Source Badge in Sentinel Mode:
     - Prominently display whether analysis was powered by `🛡️ Local ML Engine (Offline / Zero API Keys)` vs `☁️ Gemini Multimodal Vision API (Cloud)`.
   - Rahul Persona:
     - Verify ZERO occurrences of "Pushpa Devi" anywhere in user-facing text, tooltips, or comments in `app.py`. "Rahul" persona must be used consistently.
3. Verification:
   - Run python import check using `.venv\Scripts\python.exe`:
     `& .\.venv\Scripts\python.exe -c "import app; print('app imported successfully')"`
   - Verify no syntax or runtime import errors.
4. Output: Write your completion report to `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m2_v2\handoff.md` and send_message back to parent.
