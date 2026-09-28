# Dead Ends Log

| Iteration | Approach Tried | Why It Failed | Files Touched |
|-----------|---------------|---------------|---------------|
| Survey | Using pytesseract for WhatsApp screenshots | Prohibited by Requirement R1; requires external C++ binary `tesseract.exe`; Gemini natively supports multimodal image inputs | requirements.txt, backend.py |
| Survey | Writing gTTS audio to disk via NamedTemporaryFile | Causes Windows file locking `[WinError 32]` and disk leaks; in-memory `io.BytesIO` must be used instead | backend.py, app.py |
| Survey | Dark neon cyberpunk styling in app.py | Violates Requirement R5 and GovTech portal specification (must be clean white/blue State Cyber Police portal) | app.py |
