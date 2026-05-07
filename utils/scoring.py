import re
from math import sqrt
from utils.gemini_api import get_embedding

# -------------------------
# CONTACT EXTRACTION
# -------------------------
def extract_contact_details(text):
    # EMAIL
    email_match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    email = email_match[0] if email_match else "Not Found"

    # PHONE (simple international pattern)
    phone_match = re.findall(r"\+?\d[\d \-\(\)]{7,}\d", text)
    phone = phone_match[0] if phone_match else "Not Found"

    # NAME: first non-empty line, cleaned
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    name = lines[0][:60] if lines else "Unknown"

    return name, email, phone

# -------------------------
# COSINE SIMILARITY
# -------------------------
def cosine_sim(a, b):
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sqrt(sum(x * x for x in a))
    mag_b = sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def jd_similarity(resume_text, jd_text):
    try:
        emb1 = get_embedding(resume_text)
        emb2 = get_embedding(jd_text)
        return cosine_sim(emb1, emb2)
    except Exception:
        # fallback: token overlap
        r_tokens = set(re.findall(r"\b[a-z0-9]+\b", resume_text.lower()))
        jd_tokens = set(re.findall(r"\b[a-z0-9]+\b", jd_text.lower()))
        if not jd_tokens:
            return 0.0
        return len(r_tokens & jd_tokens) / len(jd_tokens)

# -------------------------
# SKILLS MATCH
# -------------------------
def skills_match(text, skills):
    skills_list = [s.strip().lower() for s in re.split(r"[,\n;]+", skills) if s.strip()]
    found = []
    lower = text.lower()
    for s in skills_list:
        if s and s in lower:
            found.append(s)
    score = len(found) / len(skills_list) if skills_list else 0.0
    return score, found

# -------------------------
# SCORE RESUME
# -------------------------
def score_resume(text, jd, skills):
    jd_score = jd_similarity(text, jd) if jd else 0.0
    skills_score, matched = skills_match(text, skills) if skills else (0.0, [])
    return jd_score, skills_score, matched

# -------------------------
# AGGREGATE & SAVE CSV
# -------------------------
def aggregate_scores(jd_score, skills_score, w1=0.6, w2=0.4):
    return jd_score * w1 + skills_score * w2

def save_shortlist_csv(rows, path):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename", "name", "email", "phone",
            "jd_score", "skills_score", "matched_skills",
            "total_score", "category"
        ])
        for r in rows:
            writer.writerow([
                r.get("filename", ""),
                r.get("name", ""),
                r.get("email", ""),
                r.get("phone", ""),
                r.get("jd_score", 0.0),
                r.get("skills_score", 0.0),
                ",".join(r.get("matched_skills", [])),
                r.get("total_score", 0.0),
                r.get("category", "")
            ])
