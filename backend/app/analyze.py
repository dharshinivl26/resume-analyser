from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import fitz  # pymupdf
import docx

from app.skill_extractor import extract_skills

router = APIRouter(prefix="/analyze", tags=["Analyze"])


# ---------- PDF ----------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text


# ---------- DOCX ----------
def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(file_bytes)
    return "\n".join(p.text for p in doc.paragraphs)


# ---------- ANALYZE ----------
@router.post("/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if resume.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX allowed")

    file_bytes = await resume.read()

    resume_text = (
        extract_text_from_pdf(file_bytes)
        if resume.filename.lower().endswith(".pdf")
        else extract_text_from_docx(file_bytes)
    )

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text could not be extracted")

    # ---- SKILL MATCHING ----
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))

    ats_score = int((len(matched_skills) / max(len(jd_skills), 1)) * 100)

    return {
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
