import json
from datetime import date
with open(r"E:\redrob-candidate-ranker\candidates.jsonl","r",encoding="utf-8") as f:
    all_candidates= [json.loads(line) for line in f if line.strip()]



def is_honeypot(candidate):
    
    # Check 1
    total_months = 0
    for job in candidate["career_history"]:
        total_months += job["duration_months"]
    claimed_months = candidate["profile"]["years_of_experience"] * 12
    if total_months > claimed_months * 1.5:
        return True
    
    # Check 2
    zero_proof_experts = 0
    for skill in candidate["skills"]:
        if skill["proficiency"] == "expert":
            if skill["endorsements"] == 0 and skill.get("duration_months", 0) == 0:
                zero_proof_experts += 1
    if zero_proof_experts >= 2:
        return True
    
    # Check 3
    from datetime import date
    for job in candidate["career_history"]:
        start = date.fromisoformat(job["start_date"])
        months_since_start = (date.today() - start).days / 30
        if job["duration_months"] > months_since_start + 3:
            return True
    
    return False


# Test
honeypots_found = 0
for candidate in all_candidates:
    if is_honeypot(candidate):
        honeypots_found += 1

print(f"Honeypots found in 100K: {honeypots_found}")