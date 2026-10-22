# RakshaSite — AI-Powered Construction Safety & Compliance Monitoring

RakshaSite is an intelligent video analytics and automated compliance monitoring system designed for Indian construction sites. It detects Personal Protective Equipment (PPE) violations using YOLOv8, assesses severity using machine learning, maps violations to Indian labor safety laws (BOCW Act, 1996) via RAG, and generates automated compliance reports.

---

## 🏗️ System Architecture
```text
Video Input → YOLO Detection → Detection Agent → Risk Agent → Compliance Agent (RAG) → Report Agent (LLM) → Dashboard & DB
```

1. **YOLO Detection**: Real-time object detection recognizing Workers, Hardhats, Safety Vests, and non-compliance states.
2. **Detection Agent**: Temporal smoothing & multi-frame tracking to eliminate transient false alarms.
3. **Risk Agent**: Multi-factor severity scoring (Zone, Height, Weather, Workers) classifying risk levels (LOW, MEDIUM, HIGH, CRITICAL).
4. **Compliance Agent (RAG)**: Semantic vector retrieval over the Building and Other Construction Workers (BOCW) Act, 1996 via ChromaDB.
5. **Report Agent**: LLM-driven structured incident and compliance report generation.
6. **Dashboard & API**: FastAPI backend powering an interactive React dashboard.

---

## 📁 Project Directory Structure
```
rakshasite/
├── README.md               # Project overview and setup instructions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
├── configs/
│   └── config.yaml         # Central pipeline configuration
├── data/
│   ├── raw/                # Original downloaded datasets (Roboflow, SH17)
│   └── unified/            # Merged 5-class YOLO training dataset
├── src/
│   ├── detection/          # YOLOv8 inference & tracking logic
│   ├── agents/             # LangGraph agent orchestration
│   ├── rag/                # BOCW Act retrieval & ChromaDB vector store
│   ├── database/           # SQLite/PostgreSQL models & operations
│   └── utils/              # Helper utilities & logging
├── backend/                # FastAPI REST API server
├── frontend/               # React + Vite dashboard
├── models/                 # Model checkpoints (.pt, .onnx)
├── knowledge_base/         # BOCW Act legal texts and documents
├── tests/
│   └── test_cases.json     # 50 validation test scenarios
└── reports/                # Generated compliance PDF reports
```

---

## 🚀 Quickstart

### 1. Environment Setup
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
```

### 2. Dataset Harmonization
To regenerate the unified dataset from raw sources:
```bash
python scratch/merge_datasets.py
```

### 3. Model Training
Train YOLOv8 on the unified 5-class dataset:
```bash
yolo detect train data=data/unified/data.yaml model=yolov8m.pt epochs=50 imgsz=640
```
