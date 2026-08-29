import json
import time
import requests
import os

API_URL = "http://localhost:8000/api/v1/rank"
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "data_pipeline", "mock_cohort.json")

def main():
    print(f"Loading data from {MOCK_DATA_PATH}...")
    
    # Wait for the API to be ready if running via docker-compose
    health_url = "http://localhost:8000/health"
    max_retries = 5
    for i in range(max_retries):
        try:
            resp = requests.get(health_url)
            if resp.status_code == 200:
                print("API is up and running.")
                break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                print("Could not connect to the API. Make sure it's running.")
                return
            print("Waiting for API to start...")
            time.sleep(2)

    try:
        with open(MOCK_DATA_PATH, "r") as f:
            patients_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {MOCK_DATA_PATH} not found.")
        print("Please run data_pipeline/generate_synthetic.py first.")
        return

    # Extract just the ID and score for the ranking API
    # The API expects: {"patients": [{"patient_id": "...", "risk_score": 1.23}, ...]}
    print(f"Loaded {len(patients_data)} patients. Preparing request payload...")
    
    patients_payload = []
    for p in patients_data:
        # Pass full patient object structure so API can calculate exact scores across metrics
        patients_payload.append(p)

    print(f"Sending {len(patients_payload)} patients to the C Engine via FastAPI...")
    
    start_time = time.time()
    response = requests.post(API_URL, json={"patients": patients_payload})
    end_time = time.time()
    
    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        return
        
    result_data = response.json()
    ranked_patients = result_data.get("ranked_patients", [])
    
    print(f"\n==========================================================================")
    print(f"RANKING COMPLETED IN {(end_time - start_time) * 1000:.2f} ms")
    print(f"ENGINE: {result_data.get('engine')} (C Core Time: {result_data.get('c_core_execution_time_ms', 0)} ms)")
    print(f"TOTAL PATIENTS PROCESSESSED: {len(ranked_patients)}")
    print(f"==========================================================================\n")

    for i, p in enumerate(ranked_patients, start=1):
        triage = p.get("cognipath_triage", {})
        score = triage.get("risk_score", p.get("risk_score", 0.0))
        tier = triage.get("risk_tier", "HIGH" if score >= 15 else "MODERATE" if score >= 5 else "LOW")
        
        # Mark Top 10 High Risk distinctly, Moderate separately, Low separately
        if i <= 10:
            status = "*** [TOP 10 HIGH RISK - CRITICAL ATTENTION] ***"
        elif tier == "HIGH" or score >= 15.0:
            status = "[HIGH RISK]"
        elif tier == "MODERATE" or score >= 5.0:
            status = "[MODERATE RISK]"
        else:
            status = "[LOW RISK]"
            
        print(f"Rank #{i:<3} | Patient: {p['patient_id']} | Risk Score: {score:<6.2f} | Status: {status}")

if __name__ == "__main__":
    main()