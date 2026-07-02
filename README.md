# Redrob Candidate Ranker

A Python-based candidate ranking system that evaluates job applicants based on their technical skills, work experience, career history, and recruiter signals. The project generates a ranked list of candidates for a given job description and exports the results as a submission CSV.

---

## Project Structure

```
redrob-candidate-ranker/
│
├── data/
│   └── sample_candidates.json
│
├── explore.py                 # Dataset exploration and analysis
├── rank.py                    # Candidate scoring and ranking
├── honeypot.py                # Honeypot profile detection
├── validate_submission.py     # Submission validator
├── submission.csv             # Generated ranked candidates
├── requirements.txt
└── README.md
```

---

## Features

- Exploratory Data Analysis (EDA) on candidate dataset
- Technical vs Non-Technical title classification
- Product company experience detection
- Skill matching with Job Description
- Behavioral score adjustment using recruiter signals
- Honeypot profile filtering
- Final candidate ranking
- CSV submission generation

---

## Scoring Strategy

The final score is calculated using multiple factors.

### 1. Career Score

Candidates receive additional points for:

- Product company experience
- Relevant industries
- Penalized if entire career is in IT Services/Consulting

Example:

- Product company experience → +10
- Entire consulting career → -8

---

### 2. Skill Score

The project matches candidate skills against required Job Description skills.

Current weighted skills include:

| Skill | Weight |
|--------|-------:|
| Embeddings | 10 |
| Vector Databases | 10 |
| Retrieval | 10 |
| Ranking | 9.5 |
| NLP | 8 |
| Fine Tuning | 7 |
| Evaluation | 6 |
| Python | 6 |

Trust score is calculated using:

- Skill assessment score
- Endorsements
- Duration of experience
- Proficiency level

---

### 3. Experience Score

Candidates with ideal experience receive bonus points.

| Experience | Score |
|------------|------:|
| 5–9 years | 10 |
| 3–5 years | 5 |
| Others | 0 |

---

### 4. Behavioral Multiplier

The final score is adjusted using recruiter signals.

Factors include:

- Open to work
- Recruiter response rate
- Notice period
- GitHub activity
- Last active date

Example adjustments:

- Open to work → ×1.10
- Notice ≤30 days → ×1.10
- High GitHub activity → ×1.15
- Inactive profile → penalty
- Low recruiter response rate → penalty

---

### 5. Honeypot Detection

Suspicious or fake profiles are detected using `honeypot.py`.

If a candidate is identified as a honeypot:

```
Final Score = 0
```

---

## Final Score Formula

```
Final Score =
(Career Score
 + Skill Score
 + Experience Score)
× Behavioral Multiplier
```

---

## Dataset Exploration

`explore.py` provides useful insights including:

- Country distribution
- Candidates from India
- Open-to-work statistics
- Experience distribution
- GitHub activity
- Most common job titles
- Skill assessment availability
- Notice period distribution
- Recently active candidates
- Industry distribution

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Explore Dataset

```bash
python explore.py
```

## How to Reproduce

```bash
python rank.py
```

This will:
1. Load `candidates.jsonl` from the project directory
2. Score all 100,000 candidates
3. Generate `submission.csv` with top 100 ranked candidates
---

## Output Format

The generated CSV contains:

| Column | Description |
|---------|-------------|
| candidate_id | Unique candidate ID |
| rank | Candidate rank |
| score | Final computed score |
| reasoning | Short explanation for ranking |

---

## Technologies Used

- Python 3
- JSON
- CSV
- Collections (Counter)
- Datetime

---

## Future Improvements

- Machine Learning based ranking
- Semantic skill matching using embeddings
- Resume parsing
- Configurable scoring weights
- Streamlit dashboard
- LLM-powered reasoning for ranking

---

## Author

**Meenakshi Gupta**

B.Tech CSE (AI & ML)

Candidate Ranking System for Redrob Assignment
