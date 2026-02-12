from fastapi import APIRouter, HTTPException
import hashlib
import secrets
from database import get_db
from models import UserLogin, UserRegister, UserOut

router = APIRouter()

TOKEN_STORE = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_token(token: str) -> dict:
    if token not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Неверный токен")
    return TOKEN_STORE[token]


@router.post("/login")
def login(data: UserLogin):
    db = get_db()
    user = db.execute(
        "SELECT u.*, r.name as role_name FROM users u JOIN roles r ON u.role_id = r.id WHERE u.username = ?",
        (data.username,)
    ).fetchone()
    db.close()

    if not user or user["password_hash"] != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Учётная запись деактивирована")

    token = secrets.token_hex(32)
    TOKEN_STORE[token] = {
        "user_id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role_id": user["role_id"],
        "role_name": user["role_name"],
    }

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role_id": user["role_id"],
            "role_name": user["role_name"],
        }
    }


@router.post("/register")
def register(data: UserRegister):
    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE username = ?", (data.username,)).fetchone()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

    db.execute(
        "INSERT INTO users (username, password_hash, full_name, role_id) VALUES (?, ?, ?, ?)",
        (data.username, hash_password(data.password), data.full_name, data.role_id or 2)
    )
    db.commit()
    db.close()
    return {"message": "Регистрация прошла успешно"}


@router.get("/me")
def get_me(token: str):
    user_data = verify_token(token)
    return user_data


@router.post("/logout")
def logout(token: str):
    if token in TOKEN_STORE:
        del TOKEN_STORE[token]
    return {"message": "Выход выполнен"}
