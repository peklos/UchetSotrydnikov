from fastapi import APIRouter, HTTPException
from database import get_db
from models import UserUpdate
from routers.auth import hash_password

router = APIRouter()


@router.get("/users")
def get_users():
    db = get_db()
    rows = db.execute("""
        SELECT u.id, u.username, u.full_name, u.role_id, r.name as role_name, u.is_active, u.created_at
        FROM users u
        JOIN roles r ON u.role_id = r.id
        ORDER BY u.id
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/roles")
def get_roles():
    db = get_db()
    rows = db.execute("SELECT * FROM roles ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    db = get_db()
    updates = []
    params = []

    if data.full_name is not None:
        updates.append("full_name = ?")
        params.append(data.full_name)
    if data.role_id is not None:
        updates.append("role_id = ?")
        params.append(data.role_id)
    if data.is_active is not None:
        updates.append("is_active = ?")
        params.append(data.is_active)

    if not updates:
        db.close()
        return {"message": "Нет данных для обновления"}

    params.append(user_id)
    db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
    db.commit()
    db.close()
    return {"message": "Пользователь обновлён"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    db.close()
    return {"message": "Пользователь удалён"}


@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: int):
    db = get_db()
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password("password123"), user_id))
    db.commit()
    db.close()
    return {"message": "Пароль сброшен на password123"}


@router.get("/stats")
def admin_stats():
    db = get_db()
    users_count = db.execute("SELECT COUNT(*) as cnt FROM users").fetchone()["cnt"]
    active_users = db.execute("SELECT COUNT(*) as cnt FROM users WHERE is_active = 1").fetchone()["cnt"]
    employees_count = db.execute("SELECT COUNT(*) as cnt FROM employees").fetchone()["cnt"]
    events_count = db.execute("SELECT COUNT(*) as cnt FROM staff_events").fetchone()["cnt"]
    db.close()
    return {
        "users_count": users_count,
        "active_users": active_users,
        "employees_count": employees_count,
        "events_count": events_count,
    }
