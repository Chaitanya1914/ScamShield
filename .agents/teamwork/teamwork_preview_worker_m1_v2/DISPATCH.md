## 2026-10-01T04:25:34Z
You are Worker M1 (Backend Integration & Local ML Primary Engine).
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m1_v2
Workspace root: c:\Users\chait\OneDrive\Desktop\Scam Shield
Parent Orchestrator ID: 4f70409b-f3dd-4265-ba60-566f458cbcc3

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY FIRST STEP: Read:
1. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md (especially section "## 2026-10-01T01:42:44Z")
2. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md
3. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_1\handoff.md
4. c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_2\handoff.md

Your Exclusive File Write Boundaries: `backend.py`, `scam_detector.py`. Do NOT edit other files.

Your Mission:
1. In `scam_detector.py`:
   - Inspect existing `scam_detector.py` and `scamshield_model.pkl` (pre-trained model is already at workspace root).
   - Fix `_load()`: handle corrupt/invalid pickle safely without crash. If load fails, attempt `train()` if dataset exists, or fall back to rule-based engine. Ensure `self.tfidf` is never accessed when None.
   - Fix `extract_red_flags`: for safe messages (`risk == "Low"` or no flags), return `[]` (empty list), NOT `["No critical red flags detected..."]`, ensuring `len(red_flags) == 0`.
   - Add `get_metrics()` returning dictionary: `{"status": "Trained & Loaded", "accuracy": f"{round(self.cv_score*100, 1)}%", "f1_score": f"{round(self.f1_score, 3)}", "samples": self.dataset_size, "engine": "ScamShield Local ML (Offline / Zero API Keys)", "timestamp": self.training_timestamp}`.
   - Upgrade regex extractors: phone numbers (handles dots, spaces, +91, 0), strict UPI VPAs (differentiating bank handles from email domains), and defanged scam URLs as specified in Explorer 1's handoff.
2. In `backend.py`:
   - Import `detector` from `scam_detector.py`.
   - Refactor `analyze_threat(text=..., image=..., api_key=...)`:
     - Make Local ML the PRIMARY detection engine: If `text` is provided and no image, call `detector.predict(text)` directly with ZERO API keys and ZERO internet connection. Return the normalized threat dict with `"detection_source": "local_ml"`.
     - If `image` is provided: use Gemini multimodal vision if API key is present (`detection_source: "gemini_multimodal"`), or fallback to deterministic offline image heuristics if key is missing (`detection_source: "offline_fallback"`).
     - Ensure `_normalize_threat_schema` enforces `red_flags = []` and `psychological_tactics = []` when `risk_level == "Low"`.
     - In `log_threat`: write threat logs with formula injection protection (prefixing `=`, `+`, `-`, `@`, `\t`, `\r` with `'`). Support headers cleanly.
     - In `backend.py` docstring line 8: replace any mention of "Pushpa Devi" with "Rahul".
     - Add docstrings to all public functions. Expose `get_model_metrics()` which calls `detector.get_metrics()`.
3. Verification:
   - Run existing verification scripts using `.venv\Scripts\python.exe`:
     `& .\.venv\Scripts\python.exe verify.py`
     `& .\.venv\Scripts\python.exe test_backend_m1.py`
     Ensure both PASS with exit code 0.
4. Output: Write your completion report to `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m1_v2\handoff.md` and send_message back to parent.
