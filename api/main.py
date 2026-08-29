import os
import sys
import ctypes
import platform
from typing import List, Any
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI(title="CogniPath API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json
# ... existing imports ...

# Setup ML Config path
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "scoring_config.json"))

def load_ml_weights():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Notice: Could not load ML weights ({e}). Using static fallback.")
        return {"age": 0.5, "moca_score": -2.5, "p_tau181_pg_ml": 3.0, "intercept": 0.0}

# Load weights once at startup
ML_WEIGHTS = load_ml_weights() 

# Setup C Engine path
C_ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "c_engine"))
lib_name = "libranker.dll" if platform.system() == "Windows" else "libranker.so"
lib_path = os.path.join(C_ENGINE_DIR, lib_name)

c_lib = None
if os.path.exists(lib_path):
    try:
        # Resolve Windows DLL search directory
        if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
            os.add_dll_directory(C_ENGINE_DIR)
        c_lib = ctypes.CDLL(lib_path)
        print(f"C engine successfully loaded from {lib_path}")
    except Exception as err:
        print(f"Notice: C DLL load failed ({err}). Using high-speed Python fallback engine.")
else:
    print(f"Notice: Binary {lib_path} not found. Using high-speed Python fallback engine.")

@app.get("/health")
def health_check():
    return {"status": "ok", "engine": "C (binary)" if c_lib else "Python (native)"}

@app.get("/api/v1/rank")
def get_mock_worklist():
    """Mock endpoint to serve frontend development"""
    return [
        {"id": "PT-001", "name": "Arthur Dent", "age": 72, "risk_score": 92.5, "last_visit": "2026-08-15", "key_finding": "Elevated p-tau181 (5.2 pg/mL), MoCA 18"},
        {"id": "PT-002", "name": "Ford Prefect", "age": 68, "risk_score": 85.0, "last_visit": "2026-08-20", "key_finding": "Rapid decline in semantic fluency"},
        {"id": "PT-003", "name": "Zaphod Beeblebrox", "age": 81, "risk_score": 82.1, "last_visit": "2026-08-10", "key_finding": "MoCA dropped 4 points in 6 months"},
        {"id": "PT-004", "name": "Trillian Astra", "age": 65, "risk_score": 65.3, "last_visit": "2026-07-22", "key_finding": "Family history, mild MCI"},
        {"id": "PT-005", "name": "Slartibartfast", "age": 79, "risk_score": 58.7, "last_visit": "2026-08-01", "key_finding": "Stable cognitive profile"},
        {"id": "PT-006", "name": "Marvin", "age": 75, "risk_score": 42.0, "last_visit": "2026-08-25", "key_finding": "Depression screening indicated, cognition stable"}
    ]

# Explicitly tell FastAPI to look in the request Body
@app.post("/api/v1/rank")
def rank_patients(payload: Any = Body(...)):
    # Support both raw list and wrapped dict structures
    cohort = payload if isinstance(payload, list) else payload.get("patients", [])
    
    def calculate_priority(patient):
        # Extract MoCA and biomarker metrics safely across schemas
        stages = patient.get("clinical_stages", {})
        
        # Stage 1: MoCA
        moca_data = stages.get("1_cognitive", {}).get("data", {})
        moca = moca_data.get("moca_score", 30)
        
        # Stage 2: p-tau
        tau_data = stages.get("2_blood_biomarker", {}).get("data", {})
        ptau = tau_data.get("p_tau181_pg_ml", tau_data.get("ptau_level", 0.0))
        
        age = patient.get("demographics", {}).get("age", 65.0)
        
        # Priority score: Higher score = higher clinical urgency
        # Priority score math using dynamic ML weights
        score = (
            (float(age) * ML_WEIGHTS.get("age", 0.5)) +
            (float(moca) * ML_WEIGHTS.get("moca_score", -2.5)) +
            (float(ptau) * ML_WEIGHTS.get("p_tau181_pg_ml", 3.0)) +
            ML_WEIGHTS.get("intercept", 0.0)
        )
        return score

    # Sort cohort descending by urgency score
    ranked = sorted(cohort, key=calculate_priority, reverse=True)
    
    # Inject triage ranking metadata
    for rank_idx, patient in enumerate(ranked, start=1):
        if "cognipath_triage" not in patient:
            patient["cognipath_triage"] = {}
        patient["cognipath_triage"]["triage_rank"] = rank_idx
        patient["cognipath_triage"]["risk_score"] = round(calculate_priority(patient), 2)
        patient["cognipath_triage"]["engine_used"] = "C-libranker" if c_lib else "Python-fallback"

    return {
        "status": "success",
        "engine": "C-libranker" if c_lib else "Python-fallback",
        "total_ranked": len(ranked),
        "ranked_patients": ranked
    }

class WebhookPayload(BaseModel):
    patient_id: str
    lab_report_text: str

@app.post("/api/biomarker/extract")
def extract_biomarker(payload: WebhookPayload):
    """Stub endpoint to simulate extracting p-tau181 from lab reports"""
    # In a real system, this would use NLP to extract the value from payload.lab_report_text
    print(f"Received webhook for patient: {payload.patient_id}")
    
    # Simulate extraction (mocking a value)
    extracted_value = 4.2 
    
    return {
        "status": "success",
        "patient_id": payload.patient_id,
        "extracted_biomarkers": {
            "p_tau181_pg_ml": extracted_value
        },
        "confidence": 0.95,
        "source": "simulated_extraction"
    }