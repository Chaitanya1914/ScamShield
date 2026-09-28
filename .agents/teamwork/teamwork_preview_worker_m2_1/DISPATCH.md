# Dispatch — Worker M2 (GovTech Streamlit Web UI Overhaul)

**Working Directory**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m2_1`
**Project Blueprint**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md`
**Original Request**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md`
**Backend Module**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py`
**UI Specifications**: `c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_3\report.md`

## Write Ownership
You exclusively own:
- `c:\Users\chait\OneDrive\Desktop\Scam Shield\app.py`

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Tasks
1. Read `ORIGINAL_REQUEST.md`, `PROJECT.md`, and `backend.py`. Note the user requirement update: Strike Mode Honeypot persona is **Rahul** (confused 21yo college student in Hinglish), NOT Pushpa Devi.
2. Completely overhaul `app.py` to meet all R1-R5 requirements with zero dark-neon cyberpunk theme:
   - **GovTech State Cyber Police Styling**:
     - Clean, authoritative government-portal aesthetic: Deep Navy header (`#0b3b60`), Slate background (`#f8fafc`), pure white cards with soft shadows, high-contrast accessible typography.
     - Official branding header: State Cyber Crime Police / National Cyber Crime Reporting Portal (NCRP) alignment, official badge, helpline numbers (1930).
   - **Sidebar**:
     - Gemini API key input (`type="password"`) with status indicator (green badge if configured, warning with helpful instructions if empty).
     - Operating Mode Selector: **Sentinel Mode** (accessible detection & voice warning) vs **Strike Mode** (offensive Rahul honeypot).
     - Cyber Safety Guidelines & 1930 National Helpline notice.
   - **Omnichannel Input System (R1)**:
     - Tab 1: **SMS / Email Text** — multiline paste area with "Analyze Threat" button.
     - Tab 2: **WhatsApp Screenshot** — file uploader (`.png, .jpg, .jpeg`) displaying preview, calling `backend.analyze_threat(image=uploaded_file, api_key=api_key)` directly without any OCR software.
     - Tab 3: **Simulate Live Threat** — dropdown populated from `backend.load_sample_threats()` with real Hinglish scams, showing category badge and sample text, with "Load This Threat" button.
   - **Sentinel Mode Dashboard (R2 & R4)**:
     - Prominent Risk Level Badge (High: Red, Medium: Amber, Low: Green) with confidence percentage.
     - Scam Category & Recommended Action card.
     - Plain-language Red Flags list with warning icons.
     - Psychological Tactics breakdown (Urgency, Fear, Greed, Authority).
     - Extracted Scammer Identifiers table/chips (Phone Numbers, UPI IDs, Suspicious URLs).
     - **Hindi Voice Warning**: For High and Medium risk threats, generate audio via `backend.generate_voice_warning(result)` and render `st.audio(audio_bytes.getvalue(), format="audio/mp3")` with accessible audio warning card.
     - **GovTech Alert Banner (R4)**: Prominent banner confirming logging to State Cyber Police Threat Database (`threat_log.csv`) with reference ID (`#NCRP-XXXXXX`) and extracted IoC count.
   - **Strike Mode Chat UI (R3)**:
     - Interactive chat bubble UI using `st.chat_message("user")` and `st.chat_message("assistant", avatar="🧑‍🎓")`.
     - Persona: **Rahul** — naive 21yo college student stressed about exams, attendance, and hostel fees who stalls scammers with rambling Hinglish questions.
     - Initial scam message displayed, followed by Rahul's stalling reply.
     - `st.chat_input("Enter scammer's response to continue stalling...")` enabling multi-turn conversation stored in `st.session_state.strike_chat_history`.
     - "Reset Honeypot" button.
   - **Graceful Error Handling (R5)**:
     - Clear, non-crashing UI alerts if API key is missing or invalid.
     - Seamless fallback to backend offline mock mode for demonstrations and automated tests.
     - Docstrings on all helper functions in `app.py`.
3. Verify that `app.py` compiles without syntax errors:
   `.\.venv\Scripts\python.exe -m py_compile app.py`
4. Deliver `handoff.md` and notify parent.

## 2026-09-28T06:11:30Z
You are Worker M2 for the ScamShield project.
Your Working Directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m2_1
Project Blueprint: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\orchestrator\PROJECT.md
Dispatch Instructions: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_worker_m2_1\DISPATCH.md
Original Request: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md
Backend Module: c:\Users\chait\OneDrive\Desktop\Scam Shield\backend.py

Read your DISPATCH.md and ORIGINAL_REQUEST.md carefully.
Follow the MANDATORY INTEGRITY WARNING verbatim:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Overhaul app.py to implement the GovTech State Cyber Police Streamlit UI with white/blue theme, Omnichannel input tabs (text, WhatsApp image without OCR, live threat simulator from dataset), Sentinel Mode dashboard (risk level, confidence, red flags, tactics, IoCs, in-memory Hindi voice warning, cyber police alert banner), Strike Mode chat-bubbles for the Rahul honeypot persona, and graceful API key handling. Test with py_compile. Deliver handoff.md and send a message to parent when done.
