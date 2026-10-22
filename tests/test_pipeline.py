"""
PyTest Test Suite for RakshaSite Agent Pipeline
Executes test assertions directly against tests/test_cases.json using real image files and ground truth.
"""

import json
import pytest
from pathlib import Path

TEST_CASES_PATH = Path("tests/test_cases.json")

def load_test_cases():
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

test_cases = load_test_cases()

def test_total_scenarios_count():
    assert len(test_cases) == 50, f"Expected 50 test cases, found {len(test_cases)}"

@pytest.mark.parametrize("case", test_cases)
def test_image_and_label_exist(case):
    """Verify that the test case points to a valid physical image and label file on disk."""
    img_path = Path(case["image_file"])
    lbl_path = Path(case["label_file"])
    assert img_path.exists(), f"Image file missing on disk: {img_path}"
    assert lbl_path.exists(), f"Label file missing on disk: {lbl_path}"

@pytest.mark.parametrize("case", test_cases)
def test_risk_severity_consistency(case):
    """Verify that risk score strictly aligns with the severity classification label."""
    score = case["expected_risk_result"]["calculated_score"]
    label = case["expected_risk_result"]["severity_label"]
    
    if score >= 80:
        assert label == "CRITICAL"
    elif score >= 60:
        assert label == "HIGH"
    elif score >= 40:
        assert label == "MEDIUM"
    else:
        assert label == "LOW"

@pytest.mark.parametrize("case", test_cases)
def test_bocw_legal_compliance_mapping(case):
    """Verify that any detected violation maps to Section 38 of BOCW Act."""
    is_violation = case["expected_detection_result"]["is_violation"]
    sections = case["expected_compliance_result"]["applicable_bocw_sections"]
    
    if is_violation:
        assert any("Section 38" in sec for sec in sections), "Every PPE violation must cite BOCW Section 38"
        assert case["expected_compliance_result"]["penalty_clause"] is not None
    else:
        assert len(sections) == 0, "Non-violations must not have citations"
        assert case["expected_compliance_result"]["penalty_clause"] is None
