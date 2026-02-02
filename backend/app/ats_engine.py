from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.skill_extractor import extract_skills


def compute_ats_score(resume_text: str, jd_text: str):
    # -------- SKILL MATCHING --------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    skill_score = (
        len(matched_skills) / len(jd_skills)
        if jd_skills else 0
    )

    # -------- TEXT SIMILARITY --------
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors)[0][1]

    # -------- KEYWORD DENSITY --------
    keyword_density = min(len(matched_skills) / 10, 1)

    # -------- RESUME LENGTH SCORE --------
    word_count = len(resume_text.split())
    length_score = 1 if 300 <= word_count <= 900 else 0.5

    # -------- FINAL ATS SCORE --------
    ats_score = (
        skill_score * 40 +
        similarity * 35 +
        keyword_density * 15 +
        length_score * 10
    )

    return {
        "ats_score": round(ats_score, 2),
        "similarity_score": round(similarity, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "feedback": generate_feedback(missing_skills, length_score),
    }


def generate_feedback(missing_skills, length_score):
    feedback = []

    if missing_skills:
        feedback.append(
            "Add missing skills: " + ", ".join(missing_skills[:5])
        )

    if length_score < 1:
        feedback.append("Resume length should be between 300–900 words")

    feedback.append("Use strong action verbs and quantify achievements")

    return feedback
