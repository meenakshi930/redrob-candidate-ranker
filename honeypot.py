import json
from datetime import date

def is_honeypot(candidate):
    
    # Check 1 — total career months vs claimed experience
    total_months = 0
    for job in candidate["career_history"]:
        total_months += job["duration_months"]
    claimed_months = candidate["profile"]["years_of_experience"] * 12
    if total_months > claimed_months * 1.5:
        return True
    
    # Check 2 — expert skill with zero proof
    zero_proof_experts = 0
    for skill in candidate["skills"]:
        if skill["proficiency"] == "expert":
            if skill["endorsements"] == 0 and skill.get("duration_months", 0) == 0:
                zero_proof_experts += 1
    if zero_proof_experts >= 2:
        return True
    
    # Check 3 — job duration vs actual possible time
    for job in candidate["career_history"]:
        start = date.fromisoformat(job["start_date"])
        months_since_start = (date.today() - start).days / 30
        if job["duration_months"] > months_since_start + 3:
            return True
    
    return False
