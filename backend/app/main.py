from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.analyze import router as analyze_router

app = FastAPI(title="Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ auth router has NO prefix inside → add here
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# ✅ analyze router ALREADY has /analyze → DO NOT add again
app.include_router(analyze_router, tags=["Analyze"])

@app.get("/")
def root():
    return {"status": "API running"}
