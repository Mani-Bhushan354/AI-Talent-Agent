import json
import pandas as pd
from utils import extract_skills, configure_gemini

def preprocess(api_key):
    model = configure_gemini(api_key)

    df = pd.read_csv("candidate_dummy_profiles.csv")
    processed = []

    for i, row in df.iterrows():
        text = str(row.get("resume", ""))
        skills = extract_skills(model, text)

        processed.append({
            "name": f"Candidate {i+1}",
            "skills": skills,
            "experience": 3
        })

    with open("data.json", "w") as f:
        json.dump(processed, f)

    return "Processed successfully"