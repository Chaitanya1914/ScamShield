# Dispatch — Worker M3 (Verification Script verify.py Implementation)

**Working Directory**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m3_1`
**Project Blueprint**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md`
**Original Request**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md`
**Backend Module**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py`

## Write Ownership
You exclusively own:
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\verify.py`

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Tasks
1. Read `ORIGINAL_REQUEST.md` and `PROJECT.md`.
2. Implement `verify.py` in the project root according to the exact acceptance criteria:
   - Programmatically tests:
     (1) The backend analyze function `backend.analyze_threat` returns valid JSON (dict with all required keys: `risk_level`, `confidence_score`, `scam_category`, `red_flags`, `psychological_tactics`, `extracted_identifiers`, `recommended_action`, `hindi_warning_text`) when given a known scam text.
     (2) The threat logging function `backend.log_threat` creates/appends to `threat_log.csv` correctly with neutralized formula injection.
     (3) Additional smoke tests: multimodal image ingestion without OCR, in-memory `gTTS` audio generation returning `io.BytesIO`, Rahul honeypot reply generation, and Hinglish dataset sampling.
   - Self-contained and runnable directly from command line:
     `python verify.py`
   - Deterministic and offline-capable using the backend's deterministic mock engine when no live Gemini API key is in environment.
   - Output must clearly print **PASS** when all tests succeed, or **FAIL** with error details if any test fails.
   - Must exit with exit code `0` on PASS, and non-zero (e.g. `1`) on FAIL.
3. Write `verify.py` using `write_to_file`.
4. Deliver `handoff.md` and notify parent.

## 2026-09-28T06:15:42Z
You are Worker M3 for the ScamShield project.
Your Working Directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m3_1
Project Blueprint: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md
Dispatch Instructions: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m3_1\DISPATCH.md
Original Request: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md
Backend Module: c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py

Read your DISPATCH.md and ORIGINAL_REQUEST.md carefully.
Follow the MANDATORY INTEGRITY WARNING verbatim:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Implement verify.py in the project root to programmatically test backend.analyze_threat JSON structure and backend.log_threat CSV appending, printing PASS/FAIL with proper exit code (0 on PASS, 1 on FAIL). Use write_to_file to write verify.py. Deliver handoff.md and send a message to parent when done.

