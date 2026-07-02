import json
from datetime import date




def is_honeypot(candidate):
    

    total_months = 0
    for job in candidate["career_history"]:
        total_months += job["duration_months"]
    claimed_months = candidate["profile"]["years_of_experience"] * 12
    if total_months > claimed_months * 1.5:
        return True
    

    zero_proof_experts = 0
    for skill in candidate["skills"]:
        if skill["proficiency"] == "expert":
            if skill["endorsements"] == 0 and skill.get("duration_months", 0) == 0:
                zero_proof_experts += 1
    if zero_proof_experts >= 2:
        return True

    from datetime import date
    for job in candidate["career_history"]:
        start = date.fromisoformat(job["start_date"])
        months_since_start = (date.today() - start).days / 30
        if job["duration_months"] > months_since_start + 3:
            return True
    
    return False


