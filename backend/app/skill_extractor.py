import re

# ---------------- SKILLS DATABASE ----------------
SKILLS_DB = {
    "react": ["react", "reactjs", "react.js"],
    "node": ["node", "nodejs", "node.js"],
    "express": ["express", "expressjs", "express.js"],
    "mongodb": ["mongodb", "mongo", "mongo db"],
    "git": ["git", "github", "version control"],
    "javascript": ["javascript", "js"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql", "mysql", "postgresql"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
}

# ---------------- TEXT NORMALIZATION ----------------
def normalize_text(text: str) -> str:
    """
    Normalize text:
    - lowercase
    - remove special characters
    - keep tech symbols like . + #
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9.+#\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text: str) -> list:
    """
    Extract skills from text using SKILLS_DB
    Returns unique normalized skill names
    """
    text = normalize_text(text)
    found_skills = set()

    for skill, variants in SKILLS_DB.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)
                break

    return sorted(found_skills)

# ---------------- MISSING SKILLS ----------------
def get_missing_skills(resume_skills: list, jd_skills: list) -> list:
    """
    Skills required in JD but missing in resume
    """
    return sorted([skill for skill in jd_skills if skill not in resume_skills])
