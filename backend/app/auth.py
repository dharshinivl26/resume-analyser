from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt

from app.database import users_collection
from app.models import UserCreate

router = APIRouter(tags=["Auth"])

# 🔐 Password hashing (argon2 – safe & modern)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = "SECRET123"   # later move to .env
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "Signup successful"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserCreate):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"email": user.email},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}
