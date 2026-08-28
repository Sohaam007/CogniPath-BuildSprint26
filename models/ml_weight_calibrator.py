import json
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

def main():
    # Define paths
    mock_data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "data_pipeline", 
        "mock_cohort.json"
    )
    output_config_path = os.path.join(
        os.path.dirname(__file__), 
        "scoring_config.json"
    )

    # 1. Load the mock data
    if not os.path.exists(mock_data_path):
        print(f"Error: {mock_data_path} not found.")
        print("Ensure the mock data is generated first.")
        return

    print(f"Loading data from {mock_data_path}...")
    with open(mock_data_path, "r") as f:
        data = json.load(f)

    # 2. Parse into a pandas DataFrame
    # Flatten the nested JSON structure to extract the required features
    parsed_data = []
    for p in data:
        parsed_data.append({
            "patient_id": p.get("patient_id"),
            "age": p.get("age"),
            # The schema defines cognitive.moca_score
            "moca_score": p.get("cognitive", {}).get("moca_score"),
            # The schema defines biomarkers.ptau_181 (assuming this maps to p_tau181_pg_ml)
            "p_tau181_pg_ml": p.get("biomarkers", {}).get("ptau_181")
        })

    df = pd.DataFrame(parsed_data)

    # Handle missing values by imputing with the median
    df['age'] = df['age'].fillna(df['age'].median())
    df['moca_score'] = df['moca_score'].fillna(df['moca_score'].median())
    df['p_tau181_pg_ml'] = df['p_tau181_pg_ml'].fillna(df['p_tau181_pg_ml'].median())

    # 3. Create a synthetic target variable 'needs_mri'
    # 1 if MoCA < 24 and p-tau > 4.0, else 0
    df['needs_mri'] = np.where((df['moca_score'] < 24) & (df['p_tau181_pg_ml'] > 4.0), 1, 0)
    
    print(f"Data summary: {len(df)} records. Found {df['needs_mri'].sum()} cases needing MRI.")

    # 4. Train the Logistic Regression model
    features = ['age', 'moca_score', 'p_tau181_pg_ml']
    X = df[features]
    y = df['needs_mri']

    # If the target is uniform (e.g. all 1s or all 0s), the model can't train effectively
    if y.nunique() <= 1:
        print("Warning: Target variable 'needs_mri' has only one class. Using fallback weights.")
        weights = {
            "age_weight": 0.05,
            "moca_weight": -0.8,
            "ptau_weight": 0.5,
            "bias": 0.0
        }
    else:
        print("Training Logistic Regression model...")
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)

        # 5. Extract the learned coefficients
        weights = {
            "age_weight": float(model.coef_[0][0]),
            "moca_weight": float(model.coef_[0][1]),
            "ptau_weight": float(model.coef_[0][2]),
            "bias": float(model.intercept_[0])
        }

    # 6. Save these weights to models/scoring_config.json
    print(f"Learned weights:\n{json.dumps(weights, indent=2)}")
    
    with open(output_config_path, "w") as f:
        json.dump(weights, f, indent=2)
    
    print(f"Weights successfully saved to {output_config_path}")

if __name__ == "__main__":
    main()