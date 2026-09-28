# Original User Request

## 2026-09-28T04:54:13Z

Build **ScamShield** — a near-production-quality, Omnichannel AI-powered Scam & Fraud Detector web application. The app accepts suspicious messages from three vectors (SMS text, Email text, and WhatsApp screenshots via Gemini Multimodal) and provides real-time AI-powered threat analysis. It features two unique operating modes: **Sentinel Mode** (accessible voice warnings in Hindi/English via text-to-speech for elderly/vulnerable users) and **Strike Mode** (an offensive AI honeypot that generates time-wasting replies to scammers using a confused elderly persona). The app also simulates GovTech auto-reporting by logging extracted scammer identifiers (phone numbers, UPI IDs, URLs) to a local threat database CSV.

The UI must be clean, minimal, and government-portal style (white/blue color scheme, highly accessible, simple navigation) — not a flashy demo, but a tool that looks like it could be deployed by a State Cyber Police department. The codebase must have proper error handling, logging, and clean modular structure.

Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield
Integrity mode: development

**Pre-existing resources in the working directory:**
- `India_Cyber_Scam_Hinglish_Dataset.csv` — Kaggle dataset. Use this for pre-loaded test/demo messages.
- `test_images/` — 4 synthetic WhatsApp scam screenshots for testing the multimodal image upload.
- `.venv/` — A Python 3.11 virtual environment already exists. Install all dependencies into it.

**Important:** The app requires a Google Gemini API key to function. The key should be entered by the user through the UI (a sidebar text input). Do NOT hardcode any API keys.

## Requirements

### R1. Omnichannel Input System (Multimodal)
The web application must accept suspicious messages through three distinct input methods: (1) a text area for pasting raw SMS or Email content, (2) a file uploader for WhatsApp screenshot images (.png, .jpg, .jpeg) which passes the image directly to the Gemini API (multimodal processing, NO Tesseract), and (3) a "Simulate Live Threat" feature that loads real scam examples from the included Hinglish CSV dataset.

### R2. Sentinel Mode — AI Threat Analysis with Voice Warnings
When Sentinel Mode is active, the app must send the input (text or image) to the Gemini API for analysis and display a structured threat assessment including: risk level (High/Medium/Low), confidence score, scam category, a list of red flags in plain language, psychological tactics used by the scammer, extracted scammer identifiers, and a recommended action. For High and Medium risk messages, the app must generate and auto-play an audio warning in Hindi using `gTTS` (Text-to-Speech).

### R3. Strike Mode — Offensive AI Honeypot
When Strike Mode is active, the app must generate a time-wasting reply to the scammer. The reply should be written in Hinglish as a confused, friendly elderly Indian person (a persona named "Pushpa Devi") who believes the scam might be real but keeps asking irrelevant questions. The conversation should be displayed in a chat-bubble UI format.

### R4. GovTech Auto-Reporting Simulation
When a High or Medium risk threat is detected, the app must extract any scammer identifiers from the AI response and append them to a local CSV file (`threat_log.csv`). The UI must display a prominent alert banner confirming the threat data has been logged to the "State Cyber Police Threat Database."

### R5. Professional UI & Code Quality
The web application must use Streamlit with a clean, accessible, government-portal-style UI (white/blue color scheme). The codebase must be modular (separate backend logic from UI), include proper error handling for API failures, and include docstrings on all public functions.

## Acceptance Criteria

### Functional — Input System
- [ ] The app launches without errors via `streamlit run app.py` using the `.venv` virtual environment
- [ ] Pasting a scam SMS text returns a valid threat assessment
- [ ] Uploading `test_images/kbc_lottery_scam.png` successfully passes the image to Gemini and returns a valid threat assessment without requiring OCR software
- [ ] The "Simulate Live Threat" feature loads at least 5 distinct scam examples from the Hinglish CSV dataset

### Functional — Sentinel Mode
- [ ] Sentinel Mode displays: risk level, confidence score, scam category, red flags list, psychological tactics, extracted identifiers, and recommended action
- [ ] For a High-risk message, an audio file is generated via `gTTS` and playable in the browser
- [ ] The audio speaks in Hindi

### Functional — Strike Mode
- [ ] Strike Mode generates a Hinglish reply in the Pushpa Devi persona
- [ ] The reply is displayed in a chat-bubble format

### Functional — GovTech Reporting
- [ ] After analyzing a High-risk message, `threat_log.csv` is created/appended with extracted identifiers
- [ ] A visible alert banner appears in the UI confirming the threat was logged

### Non-Functional — UI & Code
- [ ] The UI uses a clean white/blue color scheme
- [ ] The app handles a missing or invalid Gemini API key gracefully
- [ ] Backend logic is in a separate file from the Streamlit UI code

### Verification Script
- [ ] A script `verify.py` exists that programmatically tests: (1) the backend analyze function returns valid JSON when given a known scam text, (2) the threat logging function creates/appends to `threat_log.csv` correctly. The script must print PASS/FAIL.

## Requirement Update — 2026-09-28T05:43:58Z

USER FEEDBACK / REQUIREMENT UPDATE:
Please update the Strike Mode (Honeypot) persona in the backend code. The user has requested to change the name from "Pushpa Devi" to "Rahul" or "Rohan". Please adjust the prompt accordingly (e.g., change the persona from a confused grandmother to a confused average user or college student named Rahul). Ensure this change is reflected in the final backend.py and app.py UI.

## Priority Update — Speed Mode — 2026-09-28T06:13:57Z

USER REQUEST / HIGH PRIORITY:
The user is requesting to accelerate delivery. Please enter "Speed Mode". 
Do not sacrifice core functionality (API, Voice, Logging, Strike Mode), but please skip any non-essential cosmetic polishing, redundant testing, or over-engineering in Milestone 2 and Milestone 3. Deliver the functional Streamlit UI MVP as quickly as possible.
