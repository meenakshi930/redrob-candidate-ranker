import json
import csv
from honeypot import is_honeypot
from datetime import datetime

with open("data/sample_candidates.json", "r", encoding="utf-8") as file:
    candidates = json.load(file)

def classify_title(title):
    title = title.lower()
    non_tech_keywords = ["vice president", "marketing", "sales", "business development",
                         "bd", "hr", "human resources", "finance", "accounting", "recruiter",
                         "legal", "lawyer", "operations", "admin", "administrator"]
    tech_keywords = ["engineer", "developer", "programmer", "software", "machine learning",
                     "ml", "ai", "artificial intelligence", "deep learning", "dl", "nlp",
                     "full stack", "backend", "frontend", "devops", "scientist", "architect",
                     "researcher", "technologist"]
    for keyword in non_tech_keywords:
        if keyword in title:
            return "Non-Tech"
    for keyword in tech_keywords:
        if keyword in title:
            return "Tech"
    return "ambiguous"

def classify_career(candidate):
    career = candidate["career_history"]
    product_industries = ["Software", "Fintech", "Food Delivery", "E-commerce", "AI/ML", "Transportation"]
    has_product_exp = False
    all_consulting = True
    for job in career:
        industry = job["industry"]
        is_consulting = (industry == "IT Services")
        if not is_consulting:
            all_consulting = False
        if industry in product_industries:
            has_product_exp = True
    return {"has_product_exp": has_product_exp, "all_consulting": all_consulting}

jd_requirements = {
    "embeddings": ["embeddings", "sentence-transformers", "bge", "e5", "openai embeddings"],
    "vector_db": ["milvus", "pinecone", "faiss", "qdrant", "weaviate"],
    "retrieval": ["retrieval", "bm25", "hybrid search", "dense retrieval"],
    "ranking": ["ranking", "recommendation", "learning to rank"],
    "nlp": ["nlp"],
    "fine_tuning": ["lora", "qlora", "peft", "fine-tuning"],
    "evaluation": ["ndcg", "mrr", "map", "a/b testing"],
    "python": ["python"],
}
weights = {"embeddings": 10, "vector_db": 10, "retrieval": 10, "ranking": 9.5,
           "nlp": 8, "fine_tuning": 7, "evaluation": 6, "python": 6}

def score_skill(candidate):
    assessment_scores = candidate["redrob_signals"]["skill_assessment_scores"]
    total_score = 0
    for skill in candidate["skills"]:
        skill_name = skill["name"].lower()
        matched_requirement = None
        for requirement, keywords in jd_requirements.items():
            for keyword in keywords:
                if keyword in skill_name:
                    matched_requirement = requirement
                    break
            if matched_requirement:
                break
        if matched_requirement is None:
            continue
        base_points = weights[matched_requirement]
        if skill["name"] in assessment_scores:
            trust = assessment_scores[skill["name"]] / 100
        else:
            trust = 0
            if skill["endorsements"] > 10:
                trust += 0.4
            if skill.get("duration_months", 0) > 12:
                trust += 0.4
            if skill["proficiency"] in ["advanced", "expert"]:
                trust += 0.2
            trust = min(trust, 1.0)
        total_score += base_points * trust
    return total_score

def get_behavioral_multiplier(candidate):
    multiplier = 1.0
    sig = candidate["redrob_signals"]
    last_active = datetime.fromisoformat(sig["last_active_date"])
    days_inactive = (datetime.now() - last_active).days
    if days_inactive > 180:
        multiplier *= 0.5
    elif days_inactive > 90:
        multiplier *= 0.75
    if sig["open_to_work_flag"]:
        multiplier *= 1.1
    if sig["recruiter_response_rate"] < 0.2:
        multiplier *= 0.7
    if sig["notice_period_days"] <= 30:
        multiplier *= 1.1
    elif sig["notice_period_days"] > 90:
        multiplier *= 0.8
    if sig["github_activity_score"] > 50:
        multiplier *= 1.15
    return multiplier

def score_candidate(candidate):
    if is_honeypot(candidate):
        return 0
    title = candidate["profile"]["current_title"]
    if classify_title(title) == "Non-Tech":
        return 0
    career = classify_career(candidate)
    career_score = 0
    if career["has_product_exp"]:
        career_score += 10
    if career["all_consulting"]:
        career_score -= 8
    skill_score = score_skill(candidate)
    yoe = candidate["profile"]["years_of_experience"]
    if 5 <= yoe <= 9:
        exp_score = 10
    elif 3 <= yoe < 5:
        exp_score = 5
    else:
        exp_score = 0
    multiplier = get_behavioral_multiplier(candidate)
    final_score = (career_score + skill_score + exp_score) * multiplier
    return max(0, final_score)


if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "candidates.jsonl"
    
    with open(input_file, "r", encoding="utf-8") as f:
        all_candidates = [json.loads(line) for line in f if line.strip()]
    
    print(f"Total candidates loaded: {len(all_candidates)}")
    
    results = []
    for candidate in all_candidates:
        score = score_candidate(candidate)
        results.append((score, candidate["candidate_id"], candidate))
        
    results.sort(key=lambda x: (-x[0], x[1]))
    
    print("\nTop 10 candidates:")
    for score, cid, c in results[:10]:
        print(f"{cid} | {c['profile']['current_title']} | score: {round(score, 2)}")
    
    with open("submission.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, (score, cid, c) in enumerate(results[:100], 1):
            reasoning = (
                f"{c['profile']['current_title']} with {c['profile']['years_of_experience']:.1f} yrs exp "
                f"at {c['profile']['current_company']} ({c['profile']['current_industry']}); "
                f"notice={c['redrob_signals']['notice_period_days']}d, "
                f"response_rate={c['redrob_signals']['recruiter_response_rate']:.0%}."
            )
            writer.writerow([cid, rank, round(score, 4), reasoning])
    
    print("submission.csv generated!")
