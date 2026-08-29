import json
import os
import random
import uuid
from typing import List

sys_path = os.path.dirname(os.path.abspath(__file__))
import sys
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from schemas import PatientRecord, CognitiveAssessment, BiomarkerData, MRIImaging, PETImaging


def generate_patient() -> PatientRecord:
    # Generate some realistic-looking distributions
    age = random.randint(55, 90)
    is_healthy = random.random() > 0.5
    
    if is_healthy:
        mmse = random.uniform(26, 30)
        moca = random.uniform(25, 30)
        cdr = random.choice([0, 0.5])
        abeta = random.uniform(800, 1500)
        ptau = random.uniform(10, 30)
        apoe4 = random.choices([0, 1, 2], weights=[0.7, 0.25, 0.05])[0]
        hippo = random.uniform(6.5, 9.0)
        amyloid = random.uniform(0.9, 1.2)
    else:
        mmse = random.uniform(10, 25)
        moca = random.uniform(10, 24)
        cdr = random.choice([0.5, 1.0, 2.0])
        abeta = random.uniform(400, 800)
        ptau = random.uniform(30, 90)
        apoe4 = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
        hippo = random.uniform(4.0, 6.5)
        amyloid = random.uniform(1.2, 1.8)

    patient = PatientRecord(
        patient_id=f"PT_{uuid.uuid4().hex[:8]}",
        age=age,
        gender=random.choice(["M", "F"]),
        cognitive=CognitiveAssessment(
            mmse_score=round(mmse, 1),
            moca_score=round(moca, 1),
            cdr_score=cdr
        ),
        biomarkers=BiomarkerData(
            abeta_42=round(abeta, 1),
            ptau_181=round(ptau, 1),
            apoe4_alleles=apoe4
        ),
        mri=MRIImaging(
            hippocampal_volume=round(hippo, 2),
            brain_volume=round(random.uniform(900, 1200), 1),
            ventricle_volume=round(random.uniform(20, 60), 1)
        ),
        pet=PETImaging(
            amyloid_suvr=round(amyloid, 2),
            tau_suvr=round(random.uniform(1.0, 1.5), 2)
        )
    )
    
    # Calculate a simple baseline risk score based on features
    # This will be refined by the C engine or ML models later
    risk = (
        (30 - patient.cognitive.mmse_score) * 0.1 +
        (patient.biomarkers.ptau_181 / 50) +
        (patient.biomarkers.apoe4_alleles * 0.5) +
        (10 - patient.mri.hippocampal_volume) * 0.2 +
        (patient.pet.amyloid_suvr - 1.0)
    )
    patient.risk_score = round(min(max(risk, 0), 10), 2)
    
    return patient

def main():
    patients = [generate_patient().model_dump() for _ in range(500)]
    
    output_path = os.path.join(sys_path, "mock_cohort.json")
    with open(output_path, "w") as f:
        json.dump(patients, f, indent=2)
        
    print(f"Successfully generated {len(patients)} patient records in mock_cohort.json")


if __name__ == "__main__":
    main()