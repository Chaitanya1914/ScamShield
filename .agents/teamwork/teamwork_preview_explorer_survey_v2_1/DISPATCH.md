# Survey Explorer 1 — ML Engine & Dataset
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_1
Parent Orchestrator: 4f70409b-f3dd-4265-ba60-566f458cbcc3
Task: Investigate dataset and scam_detector.py to design local ML engine architecture achieving >=90% cv accuracy with zero API keys.

## 2026-10-01T01:45:59Z
You are ML Engine Explorer (survey instance 1).
Working directory: c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_1
Workspace root: c:\Users\chait\OneDrive\Desktop\Scam Shield
Parent Orchestrator ID: 4f70409b-f3dd-4265-ba60-566f458cbcc3

MANDATORY FIRST STEP: Read c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\ORIGINAL_REQUEST.md, especially section "## 2026-10-01T01:42:44Z".

Your Mission:
Investigate the dataset `India_Cyber_Scam_Hinglish_Dataset.csv` and existing ML code `scam_detector.py` (and `train_local_ml.py`).
Analyze:
1. Dataset structure: columns, total rows, label column (`label` or `is_scam`), category column (`category`), distribution of binary and multi-class categories (bank_kyc, police_digital_arrest, police_blackmail, lottery, amazon, aadhaar, relative), text length, language mix (Hinglish/English).
2. Existing `scam_detector.py`: how is it currently written? What features, vectorizer (TF-IDF word/char ngrams), models (LogisticRegression, MultinomialNB, SGDClassifier, LinearSVC, etc.), pipelines, and serialization (`scamshield_model.pkl`) are used?
3. What is needed to guarantee >=90% cross-validated accuracy on both binary classification and multi-class category prediction? Can a unified or dual pipeline (e.g. calibrated classifier, voting ensemble, or pipeline with TF-IDF) achieve >=90% cv-accuracy reliably and quickly?
4. How should the model be serialized (`scamshield_model.pkl`) with metadata (accuracy, F1-score, feature extractor, category labels, training timestamp)?
5. How does `scam_detector.py` handle IoC extraction (phone numbers, UPI IDs, URLs) and red flags? Are regex patterns robust against obfuscation (e.g. spaces, dots, +91)?
6. How to handle auto-loading on startup, corrupted model auto-retrain, and missing dataset graceful error handling?

Write your comprehensive findings and recommendations to:
`c:\Users\chait\OneDrive\Desktop\Scam Shield\.agents\teamwork\teamwork_preview_explorer_survey_v2_1\handoff.md`
Then use `send_message` to report back to parent `4f70409b-f3dd-4265-ba60-566f458cbcc3`.
