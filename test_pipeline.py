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
        # Assuming risk_score is at the root level as defined in the generate script
        patients_payload.append({
            "patient_id": p["patient_id"],
            "risk_score": p["risk_score"]
        })

    print(f"Sending {len(patients_payload)} patients to the C Engine via FastAPI...")
    
    start_time = time.time()
    response = requests.post(API_URL, json={"patients": patients_payload})
    end_time = time.time()
    
    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        return
        
    result_data = response.json()
    ranked_patients = result_data.get("ranked_patients", [])
    
    print(f"Ranking completed in {(end_time - start_time) * 1000:.2f} ms")
    print(f"Received {len(ranked_patients)} ranked patients.")
    print("\nTop 5 Highest Risk Patients:")
    print("-" * 40)
    for i, p in enumerate(ranked_patients[:5]):
        print(f"{i+1}. {p['patient_id']} - Score: {p['risk_score']:.2f}")

    print("\nBottom 5 Lowest Risk Patients:")
    print("-" * 40)
    for i, p in enumerate(ranked_patients[-5:]):
        # We use standard formatting to show their position relative to the end
        rank_idx = len(ranked_patients) - 5 + i + 1
        print(f"{rank_idx}. {p['patient_id']} - Score: {p['risk_score']:.2f}")

if __name__ == "__main__":
    main()