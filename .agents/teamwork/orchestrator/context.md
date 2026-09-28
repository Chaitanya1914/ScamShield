# Context & Constraints — ScamShield

## Project Information
- Project Root: `c:\Users\chait\OneDrive\Desktop\Scam Shield`
- Virtual Environment: `.venv` (Python 3.11)
- Key Files Present:
  - `India_Cyber_Scam_Hinglish_Dataset.csv`
  - `test_images/` (4 synthetic WhatsApp scam screenshots)
  - `.agents/teamwork/ORIGINAL_REQUEST.md`

## Architecture Goals
- Modular code: `backend.py` for all core logic, APIs, logging, audio generation; `app.py` strictly for Streamlit UI.
- `verify.py` for automated headless verification printing PASS/FAIL.
- No OCR engines (Tesseract is forbidden; Gemini Multimodal directly processes images).
- Clean white/blue government portal style (accessible, state cyber police styling).
- Graceful error handling if API key is missing or invalid.
