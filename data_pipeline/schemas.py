from pydantic import BaseModel, Field
from typing import Dict, Any

class Demographics(BaseModel):
    age: float
    sex: str
    education_years: int

class StageData(BaseModel):
    status: str
    data: Dict[str, Any] = Field(default_factory=dict)

class PatientRecord(BaseModel):
    patient_id: str
    demographics: Demographics
    clinical_stages: Dict[str, StageData]
    cognipath_triage: Dict[str, Any]
