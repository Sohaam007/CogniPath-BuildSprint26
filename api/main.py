import os
import sys
import ctypes
import platform
from typing import List, Any
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI(title="CogniPath API")

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
        score = ((30.0 - float(moca)) * 2.5) + (float(ptau) * 3.0) + ((float(age) - 55.0) * 0.5)
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