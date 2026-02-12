from fastapi import APIRouter, HTTPException
from database import get_db
from models import PositionCreate

router = APIRouter()


@router.get("")
def get_positions(department_id: int = None):
    db = get_db()
    if department_id:
        rows = db.execute("""
            SELECT p.*, d.name as department_name
            FROM positions p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.department_id = ?
            ORDER BY p.name
        """, (department_id,)).fetchall()
    else:
        rows = db.execute("""
            SELECT p.*, d.name as department_name
            FROM positions p
            LEFT JOIN departments d ON p.department_id = d.id
            ORDER BY p.name
        """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/{pos_id}")
def get_position(pos_id: int):
    db = get_db()
    row = db.execute("""
        SELECT p.*, d.name as department_name
        FROM positions p
        LEFT JOIN departments d ON p.department_id = d.id
        WHERE p.id = ?
    """, (pos_id,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(status_code=404, detail="Должность не найдена")
    db.close()
    return dict(row)


@router.post("")
def create_position(data: PositionCreate):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO positions (name, department_id, salary_min, salary_max, description) VALUES (?, ?, ?, ?, ?)",
        (data.name, data.department_id, data.salary_min, data.salary_max, data.description)
    )
    db.commit()
    pos_id = cursor.lastrowid
    db.close()
    return {"id": pos_id, "message": "Должность создана"}


@router.put("/{pos_id}")
def update_position(pos_id: int, data: PositionCreate):
    db = get_db()
    db.execute(
        "UPDATE positions SET name=?, department_id=?, salary_min=?, salary_max=?, description=? WHERE id=?",
        (data.name, data.department_id, data.salary_min, data.salary_max, data.description, pos_id)
    )
    db.commit()
    db.close()
    return {"message": "Должность обновлена"}


@router.delete("/{pos_id}")
def delete_position(pos_id: int):
    db = get_db()
    db.execute("DELETE FROM positions WHERE id = ?", (pos_id,))
    db.commit()
    db.close()
    return {"message": "Должность удалена"}
