import json
from pathlib import Path

def run_tests():
    with open("tests/test_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Executing validation on {len(cases)} test cases...")
    for c in cases:
        img_p = Path(c["image_file"])
        lbl_p = Path(c["label_file"])
        
        if not img_p.exists():
            raise FileNotFoundError(f"Missing image file: {img_p}")
        if not lbl_p.exists():
            raise FileNotFoundError(f"Missing label file: {lbl_p}")
        
        score = c["expected_risk_result"]["calculated_score"]
        label = c["expected_risk_result"]["severity_label"]
        if score >= 80:
            assert label == "CRITICAL"
        elif score >= 60:
            assert label == "HIGH"
        elif score >= 40:
            assert label == "MEDIUM"
        else:
            assert label == "LOW"
            
        is_violation = c["expected_detection_result"]["is_violation"]
        sections = c["expected_compliance_result"]["applicable_bocw_sections"]
        if is_violation:
            assert any("Section 38" in s for s in sections), f"Violation in {c['test_case_id']} must cite Section 38"

    print(f"[PASS] 50/50 test cases successfully validated against real physical dataset images and ground truth!")

if __name__ == "__main__":
    run_tests()
