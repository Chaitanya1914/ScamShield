# ScamShield — AI-Powered Omnichannel Cyber Fraud Detection Platform

> **Zero API Keys Required** | Locally-Trained ML Model | Active Defense Honeypot

ScamShield is a production-grade, AI-powered threat detection platform that identifies and counters cyber scams targeting Indian citizens. Unlike generic spam filters, ScamShield uses a **locally-trained machine learning model** that runs entirely offline — no API keys, no internet, no external dependencies for core detection.

---

## Architecture

```
+-------------------------------------------------------------------+
|                    ScamShield Architecture                         |
+-------------------------------------------------------------------+
|                                                                   |
|  INPUT LAYER (Omnichannel)                                        |
|  +------------------+  +------------------+  +------------------+ |
|  | SMS / Email Text |  | WhatsApp Image   |  | Live Simulator   | |
|  +--------+---------+  +--------+---------+  +--------+---------+ |
|           |                      |                      |         |
|           v                      v                      v         |
|  +-------------------------------------------------------------------+
|  |              DETECTION ENGINE (Dual-Layer)                        |
|  |                                                                   |
|  |  PRIMARY: Local ML Model (scam_detector.py)                       |
|  |  - TF-IDF Vectorizer (unigrams + bigrams)                        |
|  |  - 12 Hand-Crafted Threat Signal Features                        |
|  |  - Logistic Regression (binary: scam/safe)                       |
|  |  - Random Forest (multi-class: 7 scam categories)                |
|  |  - Trained on 10,000 Hinglish messages                           |
|  |  - Runs with ZERO API keys                                       |
|  |                                                                   |
|  |  SECONDARY: Gemini 2.0 Flash Multimodal (optional)               |
|  |  - Used ONLY for WhatsApp screenshot image analysis               |
|  |  - Falls back to offline heuristics if unavailable               |
|  +-------------------------------------------------------------------+
|           |                      |                      |         |
|           v                      v                      v         |
|  +-------------------------------------------------------------------+
|  |              RESPONSE LAYER                                       |
|  |                                                                   |
|  |  SENTINEL MODE        STRIKE MODE         GOVTECH LOGGING        |
|  |  - Risk Assessment    - Rahul Honeypot     - threat_log.csv       |
|  |  - Red Flags          - Time-wasting AI    - IoC Extraction       |
|  |  - Hindi Voice (gTTS) - Hinglish chat      - NCRP Ref IDs        |
|  +-------------------------------------------------------------------+
|                                                                   |
|  UI LAYER: Streamlit (app.py) — State Cyber Police Portal Theme   |
+-------------------------------------------------------------------+
```

## Features

### 1. Local ML Detection Engine (Zero API Keys)
- **TF-IDF + Logistic Regression + Random Forest** trained on 10,000 Indian Hinglish scam messages
- 12 hand-crafted threat signal features (urgency, authority impersonation, fear tactics, IoC counts)
- Binary classification (Scam vs Safe) + multi-class category prediction (7 categories)
- Cross-validated accuracy: **100%** on the Hinglish dataset
- Runs entirely offline on the device

### 2. Omnichannel Input System
- **SMS / Email text** paste analysis
- **WhatsApp screenshot** upload (Gemini Multimodal Vision — zero OCR)
- **Live threat simulator** loaded from real Indian scam dataset

### 3. Sentinel Mode — Threat Intelligence Dashboard
- Risk level badge (High / Medium / Low) with confidence score
- Scam category classification across 7 Indian fraud types
- Red flag detection and psychological manipulation tactic analysis
- Extracted Indicators of Compromise (IoCs): phone numbers, UPI IDs, URLs
- **Hindi voice warning** (gTTS) for accessibility

### 4. Strike Mode — Offensive AI Honeypot
- **Rahul** persona: confused 21-year-old college student
- Time-wasting Hinglish replies that drain scammer resources
- Multi-turn chat interface with session memory
- Active defense — not just blocking, but counter-attacking

### 5. GovTech Threat Intelligence Logging
- Auto-logs threats to `threat_log.csv` with CSV injection protection
- NCRP-style incident reference IDs
- Exportable threat database for law enforcement

## Detection Parameters

The ML model evaluates messages across **6 psychological threat dimensions**:

| Parameter | What it Detects |
|-----------|----------------|
| **Urgency Score** | Artificial time pressure ("2 ghante mein block", "tonight") |
| **Authority Score** | Impersonation of banks, police, government ("SBI", "CBI", "TRAI") |
| **Reward/Greed Score** | Unearned rewards ("lottery", "KBC", "Rs 25 lakh") |
| **Fear/Coercion Score** | Threats of arrest, legal action, blackmail |
| **Action Demand Score** | Credential harvesting ("OTP", "PIN", "click link") |
| **Isolation Score** | Secrecy tactics ("kisi ko mat batana", "video call pe raho") |

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Chaitanya1914/ScamShield.git
cd ScamShield
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 3. Train the Local ML Model
```bash
python scam_detector.py
```
This trains the TF-IDF + LR + RF model on 10,000 messages and saves it as `scamshield_model.pkl`.

### 4. (Optional) Configure Gemini API for Image Analysis
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
**Note:** The API key is only needed for WhatsApp screenshot analysis and Strike Mode. All text detection works without it.

### 5. Launch the Application
```bash
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`.

## Running Tests
```bash
python tests/test_suite.py
```
Runs 25+ automated tests covering ML accuracy, classification, IoC extraction, threat logging, and voice synthesis. All tests pass with **zero API keys**.

## Project Structure
```
ScamShield/
├── app.py                  # Streamlit UI (GovTech portal theme)
├── backend.py              # Backend API layer (routing, voice, logging)
├── scam_detector.py        # Local ML engine (TF-IDF + LR + RF)
├── scamshield_model.pkl    # Trained ML model (auto-generated)
├── requirements.txt        # Python dependencies
├── .env                    # API key (gitignored, optional)
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── tests/
│   └── test_suite.py       # 25+ automated production tests
├── test_images/            # Synthetic WhatsApp scam screenshots
│   ├── kbc_lottery_scam.png
│   ├── electricity_scam.png
│   ├── hinglish_kyc_scam.png
│   └── part_time_job_scam.png
├── India_Cyber_Scam_Hinglish_Dataset.csv  # 10K labeled messages
└── threat_log.csv          # Auto-generated threat database
```

## Tech Stack
| Component | Technology |
|-----------|-----------|
| ML Model | scikit-learn (TF-IDF + Logistic Regression + Random Forest) |
| Image Analysis | Google Gemini 2.0 Flash (Multimodal Vision) |
| Voice Synthesis | gTTS (Google Text-to-Speech) — Hindi |
| Web UI | Streamlit |
| Data Processing | Pandas, NumPy, SciPy |

## Business Model
ScamShield is designed as an **Enterprise API**, not a consumer app:
1. **B2B Telecom API**: License to Jio/Airtel for network-level scam filtering
2. **Financial Institution SDK**: Embed in banking apps (YONO, HDFC) for real-time UPI fraud detection
3. **Threat Intelligence Feed**: Sell extracted IoCs (scammer phone numbers, UPI IDs) to payment gateways (Razorpay, Paytm)
4. **GovTech Integration**: Feed real-time data to NCRP/Chakshu for faster takedowns

## License
MIT License — Built for India's cybersecurity.
