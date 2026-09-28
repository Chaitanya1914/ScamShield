"""
Milestone 1 Backend Unit Test Suite.
Verifies all public APIs, contract schemas, error handlers, and edge cases.
"""

import io
import os
import shutil
import tempfile
from pathlib import Path

# Set mock mode to ensure deterministic offline testing
os.environ["SCAMSHIELD_MOCK_MODE"] = "1"

import backend

def test_tesseract_elimination():
    """Verify that pytesseract is NOT imported and TESSERACT_AVAILABLE is False."""
    assert not getattr(backend, "TESSERACT_AVAILABLE", True), "TESSERACT_AVAILABLE must be False"
    assert "pytesseract" not in dir(backend), "pytesseract must not be imported in backend"
    deprecated_msg = backend.extract_text_from_image("dummy.png")
    assert "[Notice]" in deprecated_msg, f"Deprecated message expected, got: {deprecated_msg}"
    print("[PASS] test_tesseract_elimination")


def test_empty_input_analysis():
    """Verify analyze_threat handles empty inputs gracefully."""
    res = backend.analyze_threat()
    assert res["risk_level"] == "Low"
    assert res["confidence_score"] == 0.0
    assert res["scam_category"] == "No Input Provided"
    assert "extracted_identifiers" in res
    assert "phone_numbers" in res["extracted_identifiers"]
    assert "recommended_action" in res
    assert "hindi_warning_text" in res
    # Legacy keys
    assert res["confidence"] == 0
    assert "recommendation" in res
    assert "warning_message_hindi" in res
    print("[PASS] test_empty_input_analysis")


def test_scam_text_analysis():
    """Verify analyze_threat detects known Indian scam patterns."""
    text = (
        "Ji namaskar Aapka SBI bank account 2 ghante mein block ho jayega KYC pending hone ke karan. "
        "Abhi apna OTP share kijiye is number par: 9876543210 ya fir is link par click karein: http://sbi-kyc-update.com"
    )
    res = backend.analyze_threat(text=text)
    assert res["risk_level"] == "High", f"Expected High, got: {res['risk_level']}"
    assert res["confidence_score"] >= 0.8, f"Expected confidence >= 0.8, got: {res['confidence_score']}"
    assert "KYC" in res["scam_category"] or "Bank" in res["scam_category"]
    assert len(res["red_flags"]) >= 1
    assert len(res["psychological_tactics"]) >= 1
    assert "9876543210" in res["extracted_identifiers"]["phone_numbers"]
    assert any("sbi-kyc-update.com" in u for u in res["extracted_identifiers"]["urls"])
    assert res["hindi_warning_text"] is not None
    # Check dual schema
    assert res["confidence"] == int(round(res["confidence_score"] * 100))
    assert res["recommendation"] == res["recommended_action"]
    print("[PASS] test_scam_text_analysis")


def test_safe_text_analysis():
    """Verify analyze_threat classifies benign messages as Low risk."""
    safe_text = "Hello ji Beta ghar aa gaya hoon, darwaza khol do."
    res = backend.analyze_threat(text=safe_text)
    assert res["risk_level"] == "Low", f"Expected Low, got: {res['risk_level']}"
    assert "Safe" in res["scam_category"] or "Legitimate" in res["scam_category"]
    assert len(res["red_flags"]) == 0
    assert len(res["extracted_identifiers"]["phone_numbers"]) == 0
    print("[PASS] test_safe_text_analysis")


def test_image_threat_analysis():
    """Verify analyze_threat handles test image inputs."""
    images_to_test = [
        ("test_images/kbc_lottery_scam.png", "Lottery", "+91 8888888888"),
        ("test_images/electricity_scam.png", "Electricity", "9876543210"),
        ("test_images/part_time_job_scam.png", "Job", "http://bit.ly/fake-job-offer"),
        ("test_images/hinglish_kyc_scam.png", "KYC", "http://sbi-kyc-update-online.com/"),
    ]
    for path_str, cat_sub, expected_ioc in images_to_test:
        img_path = Path(path_str)
        if img_path.exists():
            res = backend.analyze_threat(image=str(img_path))
            assert res["risk_level"] == "High", f"Expected High for {path_str}, got: {res['risk_level']}"
            assert cat_sub.lower() in res["scam_category"].lower(), f"Expected {cat_sub} in {res['scam_category']}"
            all_iocs = (
                res["extracted_identifiers"]["phone_numbers"] +
                res["extracted_identifiers"]["urls"] +
                res["extracted_identifiers"]["upi_ids"]
            )
            assert any(expected_ioc in ioc for ioc in all_iocs), f"Expected {expected_ioc} in {all_iocs}"
            print(f"[PASS] test_image_threat_analysis ({path_str})")
        else:
            print(f"[SKIP] test_image_threat_analysis ({path_str} not found)")


def test_threat_logging():
    """Verify log_threat is thread-safe and mitigates CSV formula injection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_csv = Path(tmpdir) / "test_threat_log.csv"
        threat_data = {
            "risk_level": "High",
            "scam_category": "Electricity Disconnection Threat",
            "extracted_identifiers": {
                "phone_numbers": ["9876543210"],
                "urls": ["=cmd|' /C calc'!A0"],
                "upi_ids": ["@fraud_vpa"],
            }
        }
        res = backend.log_threat(threat_data, file_path=test_csv)
        assert res, "log_threat must return truthy result on High threat"
        assert res == True, "ThreatLogResult must support equality with True"
        assert isinstance(res, list), "ThreatLogResult must be a list subclass"
        assert len(res) == 3, f"Expected 3 logged identifiers, got {len(res)}"
        assert res[:2] == ["9876543210", "=cmd|' /C calc'!A0"]

        # Read CSV file and verify formula injection neutralization
        with open(test_csv, "r", encoding="utf-8") as f:
            content = f.read()

        assert "'+91" in content or "'=cmd" in content, "CSV formula prefixing must neutralize '=cmd'"
        assert "'@fraud_vpa" in content, "CSV formula prefixing must neutralize '@'"

        # Verify Low risk messages are NOT logged
        low_data = {"risk_level": "Low", "scam_category": "Safe"}
        low_res = backend.log_threat(low_data, file_path=test_csv)
        assert not low_res, "Low risk messages must not be logged"
        assert low_res == False, "Empty ThreatLogResult must support equality with False"
        print("[PASS] test_threat_logging")


def test_honeypot_rahul_persona():
    """Verify Rahul honeypot persona and stalling tactics."""
    # Test single message
    reply = backend.generate_honeypot_reply("Your electricity will be cut off tonight at 9:30 PM. Pay Rs 500 now.")
    assert isinstance(reply, str)
    assert len(reply) > 20
    assert any(term in reply.lower() for term in ["sir", "sharma", "bijli", "light", "exam", "room", "viva"])
    
    # Test multi-turn history
    history = [
        {"role": "user", "content": "Aapka SBI account block ho gaya hai. OTP batao."},
        {"role": "assistant", "content": "Bhaiya kaun sa account? Kal hi papa ne fees bheji hai."},
        {"role": "user", "content": "Jaldi OTP do warna police aayegi!"},
    ]
    multi_reply = backend.generate_honeypot_reply(history)
    assert isinstance(multi_reply, str)
    assert len(multi_reply) > 10
    print("[PASS] test_honeypot_rahul_persona")


def test_load_sample_threats():
    """Verify dynamic dataset loader returns at least 5 distinct scam categories."""
    samples = backend.load_sample_threats(n=5)
    assert isinstance(samples, list)
    assert len(samples) >= 5, f"Expected at least 5 samples, got {len(samples)}"
    categories = {s["category"] for s in samples}
    assert len(categories) >= 5, f"Expected at least 5 distinct categories, got {len(categories)}"
    for s in samples:
        assert "category" in s
        assert "message" in s
        assert "source" in s
        assert len(s["message"]) > 10
    print("[PASS] test_load_sample_threats")


def test_voice_warning_buffer():
    """Verify generate_voice_warning produces in-memory BytesIO at position 0."""
    stream = backend.generate_voice_warning("सावधान! यह एक साइबर फ्रॉड संदेश है।")
    if stream is not None:
        assert isinstance(stream, io.BytesIO), "Must return io.BytesIO stream"
        assert stream.tell() == 0, "Stream must be rewound to position 0 (seek(0))"
        data = stream.read()
        assert len(data) > 100, f"Expected audio payload, got length {len(data)}"
        print("[PASS] test_voice_warning_buffer")
    else:
        print("[SKIP] test_voice_warning_buffer (gTTS network/library offline)")


if __name__ == "__main__":
    print("Running Milestone 1 Backend Tests...")
    test_tesseract_elimination()
    test_empty_input_analysis()
    test_scam_text_analysis()
    test_safe_text_analysis()
    test_image_threat_analysis()
    test_threat_logging()
    test_honeypot_rahul_persona()
    test_load_sample_threats()
    test_voice_warning_buffer()
    print("\nALL UNIT TESTS PASSED SUCCESSFULLY!")
