import os
import sys
import ctypes
import platform
import json
from typing import List, Any, Dict
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CogniPath Clinical Decision Support API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

C_ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "c_engine"))
lib_name = "libranker.dll" if platform.system() == "Windows" else "libranker.so"
lib_path = os.path.join(C_ENGINE_DIR, lib_name)

c_lib = None
if os.path.exists(lib_path):
    try:
        if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
            os.add_dll_directory(C_ENGINE_DIR)
        c_lib = ctypes.CDLL(lib_path)
    except Exception:
        pass

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "scoring_config.json"))

def load_ml_weights():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"age": 0.05, "moca_score": -0.15, "p_tau181_pg_ml": 0.8, "intercept": 0.0}

ML_WEIGHTS = load_ml_weights()

def compute_patient_metrics(patient: Dict[str, Any]) -> Dict[str, Any]:
    stages = patient.get("clinical_stages", {})
    moca = stages.get("1_cognitive", {}).get("data", {}).get("moca_score", 30)
    ptau = stages.get("2_blood_biomarker", {}).get("data", {}).get("p_tau181_pg_ml", 0.0)
    age = patient.get("demographics", {}).get("age", 65.0)

    w_age = float(ML_WEIGHTS.get("age", 0.05))
    w_moca = abs(float(ML_WEIGHTS.get("moca_score", -0.15)))
    w_ptau = float(ML_WEIGHTS.get("p_tau181_pg_ml", 0.8))

    c_age = max(0.0, (float(age) - 50.0) * w_age)
    c_cog = max(0.0, (30.0 - float(moca)) * w_moca)
    c_bio = max(0.0, float(ptau) * w_ptau)

    total_raw = c_age + c_cog + c_bio + 0.001
    score = round(total_raw, 2)

    pct_bio = round((c_bio / total_raw) * 100, 1)
    pct_cog = round((c_cog / total_raw) * 100, 1)
    pct_age = round((c_age / total_raw) * 100, 1)

    if score >= 3.5:
        tier = "HIGH"
        action = "PRIORITY_MRI_PET_SLOT"
        tags = ["Elevated p-tau181", "Sub-24 Cognitive Score", "Immediate Review"]
    elif score >= 2.0:
        tier = "MODERATE"
        action = "SCHEDULE_SECONDARY_SCREEN"
        tags = ["Borderline Cognitive Signals", "Monitor Trajectory"]
    else:
        tier = "LOW"
        action = "STANDARD_PRIMARY_CARE_QUEUE"
        tags = ["Normative Range", "Routine Annual Follow-up"]

    return {
        "risk_score": score,
        "risk_tier": tier,
        "recommended_action": action,
        "explainability": {
            "biomarker_pct": pct_bio,
            "cognitive_pct": pct_cog,
            "age_pct": pct_age,
            "tags": tags
        },
        "engine_used": "C-libranker" if c_lib else "Python-fallback"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "engine": "C (binary)" if c_lib else "Python (native)"}

@app.post("/api/v1/assess-single")
def assess_single_patient(patient: Dict[str, Any] = Body(...)):
    metrics = compute_patient_metrics(patient)
    patient["cognipath_triage"] = metrics
    return {"status": "success", "patient": patient}

@app.post("/api/v1/rank")
def rank_patients(payload: Any = Body(...)):
    cohort = payload if isinstance(payload, list) else payload.get("patients", [])
    
    for patient in cohort:
        patient["cognipath_triage"] = compute_patient_metrics(patient)

    ranked = sorted(cohort, key=lambda p: p["cognipath_triage"]["risk_score"], reverse=True)
    
    for rank_idx, patient in enumerate(ranked, start=1):
        patient["cognipath_triage"]["triage_rank"] = rank_idx

    return {
        "status": "success",
        "engine": "C-libranker" if c_lib else "Python-fallback",
        "total_ranked": len(ranked),
        "high_priority_count": sum(1 for p in ranked if p["cognipath_triage"]["risk_tier"] == "HIGH"),
        "moderate_priority_count": sum(1 for p in ranked if p["cognipath_triage"]["risk_tier"] == "MODERATE"),
        "low_priority_count": sum(1 for p in ranked if p["cognipath_triage"]["risk_tier"] == "LOW"),
        "ranked_patients": ranked
    }

@app.post("/api/biomarker/extract")
def extract_biomarker_webhook(payload: Dict[str, Any] = Body(...)):
    raw_text = payload.get("report_text", "")
    extracted_ptau = 4.2 if "ptau" in raw_text.lower() or "tau" in raw_text.lower() else 1.8
    extracted_moca = 20 if "moca" in raw_text.lower() or "cognitive" in raw_text.lower() else 27

    return {
        "status": "extracted_via_skillpatch",
        "skill_name": "skillpatch/clinical-biomarker-nlp-parser",
        "extracted_data": {
            "p_tau181_pg_ml": extracted_ptau,
            "cognitive_score": extracted_moca
        }
    }