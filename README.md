---
title: Redrob Ranker
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
  - streamlit
pinned: false
short_description: Candidate ranking system for Redrob assignment
---

# Redrob Candidate Ranker

A Python-based candidate ranking system developed for the Redrob Candidate Ranking Challenge. The application evaluates candidates based on their skills, experience, career history, recruiter signals, and profile quality, then ranks them according to a custom scoring algorithm.

---

## Features

- Candidate ranking using a weighted scoring algorithm
- Skill matching against job requirements
- Experience-based scoring
- Product company experience detection
- Recruiter signal analysis
- Honeypot profile detection
- Dataset exploration utilities
- Streamlit web interface for uploading and ranking candidates
- CSV export of ranked candidates

---

## Project Structure

```
redrob-candidate-ranker/
│
├── app.py                     # Streamlit web application
├── rank.py                    # Candidate scoring logic
├── explore.py                 # Dataset exploration
├── honeypot.py                # Honeypot profile detection
├── validate_submission.py     # Submission validation
├── requirements.txt
├── submission.csv
├── submission_metadata.yaml
├── README.md
│
└── data/
    └── sample_candidates.json
```

---

## Scoring Criteria

Each candidate is evaluated using multiple factors.

### 1. Skill Score

Candidates receive points based on how well their technical skills match the required skills.

Examples include:

- Python
- NLP
- Embeddings
- Retrieval
- Vector Databases
- Ranking
- Fine-tuning
- Evaluation

Skill confidence is also influenced by:

- Assessment scores
- Endorsements
- Years of experience
- Skill proficiency

---

### 2. Experience Score

Additional points are awarded based on relevant years of experience.

| Experience | Score |
|------------|------:|
| 5–9 years | 10 |
| 3–5 years | 5 |
| Others | 0 |

---

### 3. Career Score

Candidates receive bonuses for:

- Product company experience
- Relevant industry background

Penalties may be applied for:

- Entire career in IT services/consulting
- Less relevant experience

---

### 4. Behavioral Multiplier

The final score is adjusted using recruiter signals such as:

- Open to work
- Notice period
- Recruiter response rate
- GitHub activity
- Last active date

---

### 5. Honeypot Detection

Suspicious or fake profiles are detected using `honeypot.py`.

Detected honeypot profiles receive a score of **0**.

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

The `explore.py` script provides useful statistics such as:

- Candidate distribution by country
- Experience distribution
- Open-to-work statistics
- GitHub activity
- Industry distribution
- Most common job titles
- Recently active candidates
- Skill assessment coverage

---

## Installation

Clone the repository and install dependencies.

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Run the Streamlit App

```bash
streamlit run app.py
```

Upload a JSON or JSONL file, and the application will display the ranked candidates.

---

### Explore the Dataset

```bash
python explore.py
```

---

### Generate Rankings

```bash
python rank.py
```

This script:

- Loads candidate data
- Computes scores
- Ranks candidates
- Generates `submission.csv`

---

## Output

The generated `submission.csv` contains:

| Column | Description |
|---------|-------------|
| candidate_id | Candidate identifier |
| rank | Candidate ranking |
| score | Final calculated score |
| reasoning | Explanation for the assigned score |

---

## Technologies Used

- Python
- Streamlit
- JSON
- CSV
- Collections
- Datetime

---

## Future Improvements

- Semantic skill matching using embeddings
- LLM-based candidate reasoning
- Resume parsing
- Configurable scoring weights
- Interactive analytics dashboard
- Machine learning-based ranking model

---

## Author

**Meenakshi Gupta**

B.Tech Computer Science (AI & ML)

Developed as part of the **Redrob Candidate Ranking Challenge**.
