import json
from collections import Counter
from datetime import datetime, timedelta
# load dataset
with open("data/sample_candidates.json","r",encoding="utf-8") as file:
    candidates = json.load(file)

country_counter=Counter()
for candidate in candidates:
    country=candidate["profile"]["country"]
    country_counter[country]+=1
print(country_counter)

# How many candidates are from India
india_count=0
for candidate in candidates:
    if candidate["profile"]["country"] == "India":
        india_count+=1
print(f"Number of candidates from India: {india_count}")

# How many have open_to_work=True?
count=0
for candidate in candidates:
    if candidate["redrob_signals"]["open_to_work_flag"]==True:
        count+=1
print(f"Number of candidates with open_to_work=True: {count}")

#Distribution of years_of_experience
buckets = {"0-3 yrs": 0, "3-6 yrs": 0, "6-9 yrs": 0, "9-12 yrs": 0, "12+ yrs": 0}
for candidate in candidates:
    yoe = candidate["profile"]["years_of_experience"]
    if yoe < 3:
        buckets["0-3 yrs"] += 1
    elif yoe < 6:
        buckets["3-6 yrs"] += 1
    elif yoe < 9:
        buckets["6-9 yrs"] += 1
    elif yoe < 12:
        buckets["9-12 yrs"] += 1
    else:
        buckets["12+ yrs"] += 1
print("Experience distribution:", buckets)
# GitHub Activity Score > 0
github_count = 0
for candidate in candidates:
 if candidate["redrob_signals"]["github_activity_score"] > 0:
     github_count += 1
print(f"Number of candidates with GitHub Activity Score > 0: {github_count}")
#Most Common Current Titles
titles_counter = Counter()
for candidate in candidates:
    title = candidate["profile"]["current_title"]
    titles_counter[title] += 1
print(titles_counter)
# Skill Assessment Scores Present
count_skill_assessment = 0
for candidate in candidates:
    if candidate["redrob_signals"]["skill_assessment_scores"]:
        count_skill_assessment += 1
print(f"Number of candidates with Skill Assessment Scores: {count_skill_assessment}")
# Notice Period Distribution
notice_buckets = {"0-30 days": 0, "31-60 days": 0, "61-90 days": 0, "90+ days": 0}
for candidate in candidates:
    days = candidate["redrob_signals"]["notice_period_days"]
    if days <= 30:
        notice_buckets["0-30 days"] += 1
    elif days <= 60:
        notice_buckets["31-60 days"] += 1
    elif days <= 90:
        notice_buckets["61-90 days"] += 1
    else:
        notice_buckets["90+ days"] += 1
print("Notice period distribution:", notice_buckets)
#Active in Last 60 Days
today=datetime.now()
sixty_days = timedelta(days=60)
active_count=0
for candidate in candidates:
    last_active = candidate["redrob_signals"]["last_active_date"]

    if last_active:
        date = datetime.fromisoformat(last_active)

        if today - date <= sixty_days:
            active_count += 1

print("Active in last 60 days:", active_count)
#  Industry distribution
industry_counter = Counter()
for candidate in candidates:
    industry = candidate["profile"]["current_industry"]
    industry_counter[industry] += 1
print("Industry distribution:", industry_counter.most_common(10))



industry_counter = Counter()
for candidate in candidates:
    for job in candidate["career_history"]:
        industry_counter[job["industry"]] += 1
print(industry_counter.most_common(20))


for candidate in candidates[:10]:
    for job in candidate["career_history"]:
        print(job["company"], "→", job["industry"])



