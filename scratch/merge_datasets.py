"""
Merge and Harmonize Script for RakshaSite Detection Datasets
Merges Roboflow and SH17 datasets into a single unified YOLO format:
data/unified/
  train/
    images/
    labels/
  val/
    images/
    labels/

Unified Classes:
0: Person
1: Hardhat
2: NO-Hardhat
3: Safety Vest
4: NO-Safety Vest
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
UNIFIED_DIR = BASE_DIR / "data" / "unified"

ROBOFLOW_DIR = RAW_DIR / "roboflow"
SH17_DIR = RAW_DIR / "sh17"

# Unified class map
UNIFIED_CLASSES = {
    0: "Person",
    1: "Hardhat",
    2: "NO-Hardhat",
    3: "Safety Vest",
    4: "NO-Safety Vest"
}

# Mapping Roboflow classes (from Roboflow data.yaml) to unified IDs
# ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'SUV', 'Safety Cone', 'Safety Vest', ...]
ROBOFLOW_MAP = {
    8: 0,   # Person -> 0
    2: 1,   # Hardhat -> 1
    5: 2,   # NO-Hardhat -> 2
    11: 3,  # Safety Vest -> 3
    7: 4    # NO-Safety Vest -> 4
}

# Mapping SH17 classes to unified IDs
# 0: Person, 1: Head (NO-Hardhat), 12: Safety-vest, 14: Helmet
SH17_MAP = {
    0: 0,   # Person -> 0
    14: 1,  # Helmet -> 1
    1: 2,   # Head -> NO-Hardhat -> 2
    12: 3   # Safety-vest -> 3
}

def create_unified_structure():
    for split in ["train", "val"]:
        (UNIFIED_DIR / split / "images").mkdir(parents=True, exist_ok=True)
        (UNIFIED_DIR / split / "labels").mkdir(parents=True, exist_ok=True)

def process_roboflow():
    print("[1/2] Processing Roboflow dataset...")
    splits = {"train": "train", "valid": "val"}
    count = 0
    
    for rf_split, target_split in splits.items():
        img_dir = ROBOFLOW_DIR / rf_split / "images"
        lbl_dir = ROBOFLOW_DIR / rf_split / "labels"
        
        if not img_dir.exists():
            continue
            
        for img_file in img_dir.glob("*.*"):
            lbl_file = lbl_dir / f"{img_file.stem}.txt"
            if not lbl_file.exists():
                continue
                
            filtered_lines = []
            with open(lbl_file, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    cls_id = int(parts[0])
                    if cls_id in ROBOFLOW_MAP:
                        unified_id = ROBOFLOW_MAP[cls_id]
                        filtered_lines.append(f"{unified_id} {' '.join(parts[1:])}\n")
                        
            if filtered_lines:
                dest_img = UNIFIED_DIR / target_split / "images" / f"rf_{img_file.name}"
                dest_lbl = UNIFIED_DIR / target_split / "labels" / f"rf_{img_file.stem}.txt"
                shutil.copy2(img_file, dest_img)
                with open(dest_lbl, "w") as out:
                    out.writelines(filtered_lines)
                count += 1
                
    print(f" -> Merged {count} images from Roboflow.")

def process_sh17(val_ratio=0.15):
    print("[2/2] Processing SH17 dataset...")
    img_dir = SH17_DIR / "images"
    lbl_dir = SH17_DIR / "labels"
    
    if not img_dir.exists() or not lbl_dir.exists():
        print("SH17 images or labels directory missing. Skipping.")
        return

    all_lbls = list(lbl_dir.glob("*.txt"))
    count = 0
    
    for idx, lbl_file in enumerate(all_lbls):
        img_candidates = [
            img_dir / f"{lbl_file.stem}.jpg",
            img_dir / f"{lbl_file.stem}.jpeg",
            img_dir / f"{lbl_file.stem}.png"
        ]
        img_file = next((p for p in img_candidates if p.exists()), None)
        if not img_file:
            continue
            
        filtered_lines = []
        with open(lbl_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                cls_id = int(parts[0])
                if cls_id in SH17_MAP:
                    unified_id = SH17_MAP[cls_id]
                    filtered_lines.append(f"{unified_id} {' '.join(parts[1:])}\n")
                    
        if filtered_lines:
            target_split = "val" if (idx % int(1 / val_ratio) == 0) else "train"
            dest_img = UNIFIED_DIR / target_split / "images" / f"sh17_{img_file.name}"
            dest_lbl = UNIFIED_DIR / target_split / "labels" / f"sh17_{img_file.stem}.txt"
            shutil.copy2(img_file, dest_img)
            with open(dest_lbl, "w") as out:
                out.writelines(filtered_lines)
            count += 1
            
    print(f" -> Merged {count} images from SH17.")

def write_unified_yaml():
    yaml_content = f"""path: {UNIFIED_DIR.as_posix()}
train: train/images
val: val/images

nc: 5
names: ['Person', 'Hardhat', 'NO-Hardhat', 'Safety Vest', 'NO-Safety Vest']
"""
    with open(UNIFIED_DIR / "data.yaml", "w") as f:
        f.write(yaml_content)
    print(f"Saved unified YAML to {UNIFIED_DIR / 'data.yaml'}")

if __name__ == "__main__":
    create_unified_structure()
    process_roboflow()
    process_sh17()
    write_unified_yaml()
    print("Dataset unification complete!")
