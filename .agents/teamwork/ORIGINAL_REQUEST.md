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

## 2026-10-01T01:42:44Z

Transform **ScamShield** from a Gemini-API-wrapper prototype into a **production-grade, self-sufficient AI scam detection platform**. The core transformation is: the PRIMARY detection engine must be a locally-trained ML model that runs with ZERO external API keys. The Gemini API becomes an OPTIONAL enhancement layer for advanced features (image analysis, conversational honeypot), not the core product.

The existing codebase has: `backend.py` (1225 lines, Gemini-dependent), `app.py` (820 lines, Streamlit UI with CSS contrast bugs), `scam_detector.py` (622 lines, untrained ML engine skeleton), and `India_Cyber_Scam_Hinglish_Dataset.csv` (10,000 labeled Hinglish messages: 5000 scam / 5000 safe, 7 scam categories). A `.venv` Python 3.11 virtual environment exists with `streamlit`, `google-generativeai`, `gTTS`, `pandas`, `Pillow`, `scikit-learn`, `scipy`, and `python-dotenv` already installed.

Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield
Integrity mode: development

## Requirements

### R1. Local ML Engine as Primary Detection (Zero API Keys)
The application must use a locally-trained machine learning model as its PRIMARY scam detection engine. The model must be trained on the included `India_Cyber_Scam_Hinglish_Dataset.csv` (10,000 messages). It must perform both binary classification (scam vs safe) and multi-class category prediction (bank_kyc, police_digital_arrest, police_blackmail, lottery, amazon, aadhaar, relative). The model must achieve ≥90% cross-validated accuracy on the dataset. The trained model must be serialized to disk (`scamshield_model.pkl`) and auto-loaded on app startup. The entire detection pipeline (text analysis, risk scoring, category prediction, IoC extraction, red flag generation) must work with ZERO API keys and ZERO internet connection. The Gemini API becomes an optional secondary layer used ONLY for: (a) WhatsApp screenshot image analysis (multimodal vision) and (b) Strike Mode conversational honeypot replies. The app must clearly indicate in the UI when results come from the local ML model vs the cloud API.

### R2. Professional UI with Zero Visual Bugs
The Streamlit UI must have zero contrast/readability issues in both light and dark mode. The API key must NEVER be visible on the frontend — it must be loaded exclusively from a `.env` file via `python-dotenv`. All text must be readable against its background in every card, banner, and section. The UI must display the ML model's training metrics (accuracy, F1-score) in the sidebar to prove to judges that a real model is running. The "Rahul" persona (not "Pushpa Devi") must be used consistently everywhere in the UI and backend code.

### R3. Comprehensive Test Suite (Brutal Audit)
A test suite must exist that programmatically validates: (a) the local ML model trains successfully and achieves ≥90% cross-val accuracy, (b) the model correctly classifies at least 5 known scam messages as High risk and 5 known safe messages as Low risk, (c) IoC extraction (phone numbers, UPI IDs, URLs) works correctly on at least 3 test cases each, (d) the threat logging system creates/appends to `threat_log.csv` with CSV injection protection, (e) the Hindi voice warning generates a valid audio stream, (f) the app launches without import errors. Every test must print explicit PASS/FAIL with the test name.

### R4. Production Architecture & Clean Code
The codebase must be modular with clear separation: ML engine (`scam_detector.py`), backend API layer (`backend.py`), and UI (`app.py`). All public functions must have docstrings. Error handling must gracefully handle: missing API key (falls back to local ML), missing dataset (clear error message), corrupted model file (auto-retrains), network failures. The `requirements.txt` must include ALL dependencies (including `scikit-learn`, `scipy`, `joblib`). A `README.md` must exist with: project description, architecture diagram (text-based), setup instructions, and how to run.

### R5. Business-Ready API Layer
The backend must expose a clean, importable Python API that could be wrapped in a REST endpoint: `analyze_threat(text=..., image=...) -> dict`. The response schema must be documented. The threat intelligence logging (`threat_log.csv`) must include: timestamp, source channel, risk level, confidence score, scam category, and all extracted IoCs. This positions the product as an enterprise API, not just a web app.

## Acceptance Criteria

### ML Model Quality
- [ ] Running `python scam_detector.py` trains the model and prints cross-validated accuracy ≥90%
- [ ] The trained model file `scamshield_model.pkl` is created on disk
- [ ] The model correctly classifies "Aapka SBI account block ho jayega KYC pending. OTP share karein 9876543210" as High risk
- [ ] The model correctly classifies "Beta ghar aa gaya hoon darwaza khol do" as Low risk
- [ ] Detection works with ZERO API key set (GEMINI_API_KEY unset or empty)

### UI Quality
- [ ] `streamlit run app.py` launches without errors
- [ ] No API key input field is visible anywhere on the frontend
- [ ] All text is readable (no white-on-white or black-on-black) in both light and dark themes
- [ ] The sidebar displays ML model metrics (accuracy, F1-score)
- [ ] The "Rahul" persona name appears consistently (zero mentions of "Pushpa Devi" in user-facing text)

### Test Suite
- [ ] Running `python tests/test_suite.py` executes all tests and prints PASS/FAIL for each
- [ ] All tests pass with ZERO API keys configured
- [ ] At least 20 individual test cases exist covering ML accuracy, IoC extraction, threat logging, voice synthesis, and import validation

### Code Quality
- [ ] `README.md` exists with setup instructions and architecture overview
- [ ] `requirements.txt` includes all dependencies needed for a fresh install
- [ ] All public functions have docstrings
- [ ] No hardcoded API keys anywhere in the codebase
- [ ] The backend gracefully handles missing API key by falling back to local ML

### Verification Script
- [ ] A script `tests/test_suite.py` exists that runs ALL acceptance tests programmatically
- [ ] The script exits with code 0 if all tests pass, code 1 if any fail
- [ ] The script works on a fresh clone with only `pip install -r requirements.txt` as setup

## Directive Update — 2026-10-01T04:20:20Z

IMPORTANT UPDATE: The user has granted full autonomy — no approvals needed. Parent agent is training the local ML model (scam_detector.py) directly and saving as scamshield_model.pkl. Focus workers on:
1. Integrating the trained model into backend.py (making it PRIMARY, Gemini OPTIONAL)
2. Fixing ALL UI contrast bugs in app.py and hiding the API key
3. Writing the brutal test suite (tests/test_suite.py) with 20+ tests
4. Creating README.md and updating requirements.txt
5. Cleaning ALL "Pushpa Devi" references — replace with "Rahul" everywhere

Do NOT re-train the ML model — scamshield_model.pkl is being trained directly. Speed is critical.
