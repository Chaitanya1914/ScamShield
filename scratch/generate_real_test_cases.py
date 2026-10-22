"""
Script to generate real-world test cases directly linked to actual validation images in data/unified/val/.
Each test case contains:
- Exact image path and label path
- Ground truth bounding boxes and detected object counts
- Violation status derived from true annotations
- Worksite environmental metadata (camera ID, zone, height, weather, time)
- Expected Risk Agent output (score and severity level)
- Expected Compliance Agent output (BOCW Act section citations)
"""

import os
import json
import random
from pathlib import Path

random.seed(42)

VAL_IMG_DIR = Path("data/unified/val/images")
VAL_LBL_DIR = Path("data/unified/val/labels")
OUTPUT_FILE = Path("tests/test_cases.json")

CLASS_NAMES = {
    0: "Person",
    1: "Hardhat",
    2: "NO-Hardhat",
    3: "Safety Vest",
    4: "NO-Safety Vest"
}

ZONES = ["GROUND_LEVEL", "SCAFFOLDING", "ROOFTOP", "CRANE_AREA", "EXCAVATION_SITE"]
WEATHER_OPTIONS = ["CLEAR", "HOT_HUMID", "OVERCAST", "RAINY", "DUSTY"]
CAMERAS = ["CAM-01-GATE", "CAM-02-TOWER", "CAM-03-FACADE", "CAM-04-BASEMENT", "CAM-05-CRANE"]

def parse_label_file(lbl_path):
    boxes = []
    class_counts = {c: 0 for c in CLASS_NAMES.values()}
    if not lbl_path.exists():
        return boxes, class_counts
    
    with open(lbl_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            cls_id = int(parts[0])
            coords = [float(p) for p in parts[1:]]
            cls_name = CLASS_NAMES.get(cls_id, f"Class_{cls_id}")
            boxes.append({
                "class_id": cls_id,
                "class_name": cls_name,
                "bbox_yolo": coords
            })
            if cls_name in class_counts:
                class_counts[cls_name] += 1
    return boxes, class_counts

def determine_violation(class_counts):
    no_helmet = class_counts["NO-Hardhat"] > 0
    no_vest = class_counts["NO-Safety Vest"] > 0
    
    # If no explicitly negative vest annotation but person exists and vest=0
    # or explicit negative flags
    if no_helmet and no_vest:
        return True, "NO_HELMET_AND_VEST"
    elif no_helmet:
        return True, "NO_HELMET"
    elif no_vest:
        return True, "NO_VEST"
    elif class_counts["Hardhat"] > 0 and class_counts["Safety Vest"] > 0:
        return False, None
    elif class_counts["Person"] > 0 and class_counts["Hardhat"] == 0:
        return True, "NO_HELMET"
    else:
        return False, None

def calculate_expected_risk(violation_type, zone, height, workers, weather):
    if not violation_type:
        return 10.0, "LOW"
    
    score = 0.0
    if violation_type == "NO_HELMET_AND_VEST":
        score += 40.0
    elif violation_type == "NO_HELMET":
        score += 30.0
    elif violation_type == "NO_VEST":
        score += 20.0
        
    if zone in ["SCAFFOLDING", "ROOFTOP"]:
        score += 15.0
    elif zone in ["CRANE_AREA", "EXCAVATION_SITE"]:
        score += 12.0
    else:
        score += 5.0
        
    score += min(height * 0.8, 20.0)
    score += min(workers * 2.0, 10.0)
    
    if weather in ["RAINY", "DUSTY"]:
        score += 8.0
    elif weather == "HOT_HUMID":
        score += 4.0
        
    score = min(max(score, 0.0), 100.0)
    
    if score >= 80:
        label = "CRITICAL"
    elif score >= 60:
        label = "HIGH"
    elif score >= 40:
        label = "MEDIUM"
    else:
        label = "LOW"
        
    return round(score, 1), label

def get_bocw_sections(violation_type, zone, height):
    if not violation_type:
        return []
    sections = ["Section 38 (Safety and Health Measures)"]
    if zone == "SCAFFOLDING" or height >= 6.0:
        sections.append("Section 40 (Safety in Scaffolding & Ladder Work)")
    if zone == "ROOFTOP" or height >= 15.0:
        sections.append("Section 39 (Safety Measures for Working at Heights)")
    if zone == "CRANE_AREA":
        sections.append("Section 44 (Duties of Employers Regarding Heavy Machinery)")
    return sections

def build_test_suite():
    images = list(VAL_IMG_DIR.glob("*.*"))
    # Select 50 diverse images
    random.shuffle(images)
    
    test_cases = []
    case_id = 1
    
    for img_path in images:
        lbl_path = VAL_LBL_DIR / f"{img_path.stem}.txt"
        if not lbl_path.exists():
            continue
            
        boxes, counts = parse_label_file(lbl_path)
        if not boxes:
            continue
            
        is_violation, vtype = determine_violation(counts)
        
        # Assign contextual environmental variables
        zone = random.choice(ZONES)
        if zone == "ROOFTOP":
            height = round(random.uniform(18.0, 35.0), 1)
        elif zone == "SCAFFOLDING":
            height = round(random.uniform(6.0, 20.0), 1)
        elif zone == "EXCAVATION_SITE":
            height = round(random.uniform(1.0, 4.0), 1)
        else:
            height = 0.0
            
        weather = random.choice(WEATHER_OPTIONS)
        camera_id = random.choice(CAMERAS)
        workers_count = max(counts["Person"], 1)
        duration_mins = random.randint(3, 45)
        
        expected_score, expected_severity = calculate_expected_risk(
            vtype, zone, height, workers_count, weather
        )
        expected_sections = get_bocw_sections(vtype, zone, height)
        
        test_case = {
            "test_case_id": f"TC_{case_id:03d}",
            "image_file": str(img_path.as_posix()),
            "label_file": str(lbl_path.as_posix()),
            "camera_id": camera_id,
            "scene_context": {
                "zone_type": zone,
                "height_meters": height,
                "weather": weather,
                "duration_minutes": duration_mins,
                "workers_detected": workers_count
            },
            "ground_truth_objects": {
                "total_bounding_boxes": len(boxes),
                "counts_by_class": counts
            },
            "expected_detection_result": {
                "is_violation": is_violation,
                "violation_type": vtype,
                "filter_consecutive_frames_required": 5
            },
            "expected_risk_result": {
                "calculated_score": expected_score,
                "severity_label": expected_severity
            },
            "expected_compliance_result": {
                "applicable_bocw_sections": expected_sections,
                "penalty_clause": "Section 47: Fine up to Rs. 2,000 and/or imprisonment up to 3 months" if is_violation else None
            }
        }
        
        test_cases.append(test_case)
        case_id += 1
        if len(test_cases) == 50:
            break
            
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2)
        
    print(f"Successfully generated {len(test_cases)} production-grade test cases linked to real images at {OUTPUT_FILE}")

if __name__ == "__main__":
    build_test_suite()
