# Plan — ScamShield Full Delivery

## Objective
Deliver ScamShield end-to-end, conforming to all R1-R5 requirements in ORIGINAL_REQUEST.md with full verification, professional Streamlit UI, robust backend, multimodal Gemini capabilities without OCR, gTTS voice warnings, Pushpa Devi honeypot chat, GovTech threat logging, and verify.py test suite passing.

## Phases
1. **Survey (Phase 0)**
   - Dispatch 3 Explorers in parallel:
     - Explorer 1: Inspect environment, packages, virtual environment (`.venv`), Python libraries, existing files (`India_Cyber_Scam_Hinglish_Dataset.csv`, `test_images/`), Gemini API requirements, and gTTS availability.
     - Explorer 2: Analyze backend architecture requirements, Gemini multimodal integration (without OCR), structured prompt engineering for threat analysis, identifier extraction, and mock/offline fallback strategy for testing.
     - Explorer 3: Analyze Streamlit frontend requirements (government portal aesthetics, white/blue theme, accessibility, session state, chat bubble UI for Strike Mode, audio playback, threat database banner).
2. **Decomposition & Project Master Blueprint (Phase 1)**
   - Synthesize explorer findings into `PROJECT.md` at root, defining feature inventory, milestone boundaries, code layout, interface contracts.
   - Setup `TEST_INFRA.md` for the parallel E2E Testing Track.
3. **Execution & Dual Track (Phase 2 & 3)**
   - E2E Testing Track: Build comprehensive multi-tier test harness (`verify.py`, unit & E2E tests).
   - Milestone 1: Backend Core, Gemini client wrapper (multimodal & text), prompt templates, JSON schema response parser, and mock/fallback testing.
   - Milestone 2: Sentinel Mode & Threat Logger (`threat_log.csv` append/write, scammer identifier regex/parser, gTTS Hindi voice warning generation & caching).
   - Milestone 3: Strike Mode Honeypot ("Pushpa Devi" Hinglish conversational agent) & "Simulate Live Threat" from `India_Cyber_Scam_Hinglish_Dataset.csv`.
   - Milestone 4: Streamlit UI (`app.py`, state management, government portal white/blue theme, input tabs: Text / WhatsApp Screenshot / Live Simulation, chat bubbles, audio player, threat banner).
4. **Final Milestone: 100% E2E Pass & Coverage Hardening (Phase 4)**
   - Run verification via workers and challengers.
   - Review and Forensic Audit.
5. **Synthesis & Final Report (Phase 5)**
   - Verify all acceptance criteria.
   - Report back to caller.
