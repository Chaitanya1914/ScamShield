# E2E Test Infra: ScamShield

## Test Philosophy
- Opaque-box, requirement-driven derived from `ORIGINAL_REQUEST.md`.
- Dual validation: Headless test suite (`verify.py` & automated unit/integration tests) + full functional verification.
- Methodology: Category-Partition + Boundary Value Analysis + Pairwise Combinatorial + Real-World Workload Scenarios.

## Feature Inventory & Test Mapping
| # | Feature | Source | Tier 1 (Isolated) | Tier 2 (Boundary) | Tier 3 (Pairwise) | Tier 4 (Workload) |
|---|---------|--------|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
| 1 | Omnichannel SMS/Email Text Input | R1 | 5 | 5 | ✓ | ✓ |
| 2 | Multimodal WhatsApp Screenshot (Zero OCR)| R1 | 5 | 5 | ✓ | ✓ |
| 3 | Live Threat Simulator (Dataset Sampler) | R1 | 5 | 5 | ✓ | ✓ |
| 4 | Sentinel Mode Structured Assessment | R2 | 5 | 5 | ✓ | ✓ |
| 5 | Hindi Voice Warnings (gTTS BytesIO) | R2 | 5 | 5 | ✓ | ✓ |
| 6 | Strike Mode Honeypot (Pushpa Devi) | R3 | 5 | 5 | ✓ | ✓ |
| 7 | GovTech Threat Logging (threat_log.csv)| R4 | 5 | 5 | ✓ | ✓ |
| 8 | Cyber Police Alert Banner Display | R4 | 5 | 5 | ✓ | ✓ |
| 9 | Streamlit UI Layout & API Key Handling | R5 | 5 | 5 | ✓ | ✓ |
| 10| Verification Script (`verify.py`) | Acceptance | 5 | 5 | ✓ | ✓ |

## Test Architecture
- Automated Verification: `verify.py` executable returning PASS/FAIL with exit code 0 on PASS, 1 on FAIL.
- Sub-checks:
  - `test_threat_analysis_json_schema()`: Validates risk_level, confidence_score, scam_category, red_flags, psychological_tactics, extracted_identifiers, recommended_action.
  - `test_threat_logging_csv()`: Verifies thread-safe append, IoC columns, CSV formula sanitization.
  - `test_gtts_audio_synthesis()`: Verifies in-memory BytesIO generation and valid MP3 magic bytes (`b'ID3'` or `b'\xff\xfb'`).
  - `test_honeypot_pushpa_devi()`: Verifies Hinglish dialect and avoidance of PII leaks.
  - `test_dataset_sampling()`: Verifies ≥5 distinct scam categories loaded from `India_Cyber_Scam_Hinglish_Dataset.csv`.
  - `test_multimodal_image_input()`: Verifies PIL image handling without OCR.
