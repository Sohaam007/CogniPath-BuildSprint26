from pydantic import BaseModel
from typing import Optional

class CognitiveAssessment(BaseModel):
    mmse_score: float
    moca_score: float
    cdr_score: float

class BiomarkerData(BaseModel):
    abeta_42: float
    ptau_181: float
    apoe4_alleles: int

class MRIImaging(BaseModel):
    hippocampal_volume: float
    brain_volume: float
    ventricle_volume: float

class PETImaging(BaseModel):
    amyloid_suvr: float
    tau_suvr: float

class PatientRecord(BaseModel):
    patient_id: str
    age: int
    gender: str
    cognitive: CognitiveAssessment
    biomarkers: BiomarkerData
    mri: MRIImaging
    pet: PETImaging
    risk_score: Optional[float] = None