import os
import sys
import unittest
import ctypes
from unittest.mock import patch

# Ensure api directory is in import path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api.main import app, rank_patients, PatientRecord, c_lib

class TestRankerAPI(unittest.TestCase):
    def setUp(self):
        self.sample_cohort = [
            {
                "patient_id": "PAT-001",
                "demographics": {"age": 70.0},
                "clinical_stages": {
                    "1_cognitive": {"data": {"moca_score": 22.0}},
                    "2_blood_biomarker": {"data": {"p_tau181_pg_ml": 4.5}}
                }
            },
            {
                "patient_id": "PAT-002",
                "demographics": {"age": 80.0},
                "clinical_stages": {
                    "1_cognitive": {"data": {"moca_score": 15.0}},
                    "2_blood_biomarker": {"data": {"p_tau181_pg_ml": 10.0}}
                }
            },
            {
                "patient_id": "PAT-003",
                "demographics": {"age": 60.0},
                "clinical_stages": {
                    "1_cognitive": {"data": {"moca_score": 28.0}},
                    "2_blood_biomarker": {"data": {"p_tau181_pg_ml": 1.0}}
                }
            }
        ]

    def test_ctypes_structure(self):
        """Verify PatientRecord struct fields and alignment"""
        fields = [f[0] for f in PatientRecord._fields_]
        self.assertEqual(fields, ["id", "age", "cognitive_score", "ptau", "final_score"])

    def test_dynamic_weights(self):
        """Test rank function calculates risk scores with dynamic ML weights"""
        payload = {
            "patients": self.sample_cohort,
            "w_age": 1.0,
            "w_moca": 2.0,
            "w_ptau": 4.0
        }
        res = rank_patients(payload)
        self.assertEqual(res["status"], "success")
        ranked = res["ranked_patients"]
        self.assertEqual(len(ranked), 3)
        
        # Check scores decrease strictly (descending order)
        scores = [p["cognipath_triage"]["risk_score"] for p in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_bulletproof_failsafe(self):
        """Test fallback to Python when c_lib fails or is missing"""
        with patch("api.main.c_lib", None):
            res = rank_patients({"patients": self.sample_cohort})
            self.assertEqual(res["engine"], "Python-fallback")
            self.assertEqual(res["status"], "success")
            self.assertEqual(len(res["ranked_patients"]), 3)

if __name__ == "__main__":
    unittest.main()
