"""
Training script for the Risk Assessment Agent tabular model.
Compares XGBoost, LightGBM, and Random Forest on the 100k construction risk dataset.
Saves the best-performing model to models/risk_model.json.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.ensemble import RandomForestClassifier

# Check for XGBoost & LightGBM
try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    import lightgbm as lgb
    HAS_LGB = True
except ImportError:
    HAS_LGB = False

DATA_PATH = Path("construction_risk_dataset_100k.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_and_evaluate():
    print(f"Loading risk dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    features = ["violation_type", "zone_type", "weather", "workers_involved", "height_meters", "duration_minutes"]
    target = "severity_label"
    
    X = df[features]
    y = df[target]
    
    categorical_cols = ["violation_type", "zone_type", "weather"]
    numeric_cols = ["workers_involved", "height_meters", "duration_minutes"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols)
        ]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    if HAS_XGB:
        models["XGBoost"] = xgb.XGBClassifier(eval_metric="mlogloss", random_state=42)
    if HAS_LGB:
        models["LightGBM"] = lgb.LGBMClassifier(random_state=42)
        
    best_model_name = None
    best_score = 0.0
    best_pipeline = None
    
    for name, clf in models.items():
        print(f"\n--- Training {name} ---")
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        # If target needs encoding for XGBoost
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        print(f"{name} Test Accuracy: {acc * 100:.2f}% | F1 Score: {f1:.4f}")
        
        if acc > best_score:
            best_score = acc
            best_model_name = name
            best_pipeline = pipeline

    print(f"\n==========================================")
    print(f"Best Model: {best_model_name} with {best_score * 100:.2f}% Accuracy!")
    print(f"==========================================")
    
    # Save model pipeline
    save_path = MODEL_DIR / "risk_model.joblib"
    joblib.dump(best_pipeline, save_path)
    print(f"Saved best model pipeline to {save_path}")

if __name__ == "__main__":
    train_and_evaluate()
