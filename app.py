import streamlit as st
import json
from rank import score_candidate

st.title("Redrob Candidate Ranker")
st.write("Upload a JSONL file to rank candidates")

uploaded_file = st.file_uploader("Upload candidates JSONL", type=["jsonl", "json"])

if uploaded_file:

    content = uploaded_file.read().decode("utf-8")
    candidates = []
    for line in content.strip().split("\n"):
        if line:
            candidates.append(json.loads(line))
    
    st.write(f"Total candidates loaded: {len(candidates)}")
    
   
    results = []
    for candidate in candidates:
        score = score_candidate(candidate)
        results.append((score, candidate["candidate_id"], candidate))
    
  
    results.sort(reverse=True)
    
    
    st.subheader("Top 10 Candidates")
    for i, (score, cid, c) in enumerate(results[:10], 1):
        st.write(f"**#{i}** {cid} | {c['profile']['current_title']} | Score: {round(score, 2)}")