from fastapi import APIRouter, HTTPException
from database import get_db
from models import DepartmentCreate

router = APIRouter()


@router.get("")
def get_departments():
    db = get_db()
    rows = db.execute("""
        SELECT d.*, COUNT(e.id) as employee_count
        FROM departments d
        LEFT JOIN employees e ON e.department_id = d.id AND e.status != 'уволен'
        GROUP BY d.id
        ORDER BY d.name
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/{dept_id}")
def get_department(dept_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM departments WHERE id = ?", (dept_id,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(status_code=404, detail="Подразделение не найдено")
    dept = dict(row)

    employees = db.execute("""
        SELECT e.id, e.last_name, e.first_name, e.middle_name, p.name as position_name, e.status
        FROM employees e
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE e.department_id = ? AND e.status != 'уволен'
        ORDER BY e.last_name
    """, (dept_id,)).fetchall()
    dept["employees"] = [dict(e) for e in employees]
    db.close()
    return dept


@router.post("")
def create_department(data: DepartmentCreate):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO departments (name, description, head_name, phone) VALUES (?, ?, ?, ?)",
        (data.name, data.description, data.head_name, data.phone)
    )
    db.commit()
    dept_id = cursor.lastrowid
    db.close()
    return {"id": dept_id, "message": "Подразделение создано"}


@router.put("/{dept_id}")
def update_department(dept_id: int, data: DepartmentCreate):
    db = get_db()
    db.execute(
        "UPDATE departments SET name=?, description=?, head_name=?, phone=? WHERE id=?",
        (data.name, data.description, data.head_name, data.phone, dept_id)
    )
    db.commit()
    db.close()
    return {"message": "Подразделение обновлено"}


@router.delete("/{dept_id}")
def delete_department(dept_id: int):
    db = get_db()
    db.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
    db.commit()
    db.close()
    return {"message": "Подразделение удалено"}
