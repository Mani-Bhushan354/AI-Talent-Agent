import json
import os
import random

def load_candidates():
    path = os.path.join(os.path.dirname(__file__), "data.json")
    if os.path.exists(path):
        return json.load(open(path))
    # Fallback dummy data so your app never crashes
    return [
        {"name": "Alex Mercer", "skills": ["python", "sql", "aws", "pandas"], "experience": 4},
        {"name": "Jordan Lee", "skills": ["java", "spring", "sql"], "experience": 2},
        {"name": "Casey Smith", "skills": ["python", "machine learning", "tableau"], "experience": 1}
    ]

def calculate_agentic_score(candidate, jd_data):
    cand_skills = set([s.lower() for s in candidate.get("skills", [])])
    critical = set([s.lower() for s in jd_data.get("critical_skills", [])])
    secondary = set([s.lower() for s in jd_data.get("secondary_skills", [])])
    
    crit_matches = cand_skills.intersection(critical)
    sec_matches = cand_skills.intersection(secondary)
    
    crit_score = (len(crit_matches) / len(critical)) * 60 if critical else 0
    sec_score = (len(sec_matches) / len(secondary)) * 20 if secondary else 0
    exp_score = 20 if candidate.get("experience", 0) >= jd_data.get("min_experience", 0) else 5
    
    total_match = round(crit_score + sec_score + exp_score, 2)
    return total_match, list(crit_matches), list(critical - cand_skills)

def get_ranked_candidates(jd_data):
    candidates = load_candidates()
    results = []

    for c in candidates:
        match_score, crit_matches, missing_crit = calculate_agentic_score(c, jd_data)
        interest_score = round(random.uniform(40, 95), 2)
        final_rank = round((match_score * 0.7) + (interest_score * 0.3), 2)
        
        decision = "🔥 Hot Match" if final_rank >= 75 else "⭐ Potential" if final_rank >= 55 else "❌ Pass"

        results.append({
            **c,
            "final_score": final_rank,
            "match_score": match_score,
            "interest_score": interest_score,
            "crit_matches": crit_matches,
            "missing_critical": missing_crit,
            "decision": decision
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)