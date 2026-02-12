from fastapi import APIRouter, HTTPException
from typing import Optional
from database import get_db
from models import StaffEventCreate

router = APIRouter()


@router.get("")
def get_events(
    employee_id: Optional[int] = None,
    event_type: Optional[str] = None,
    sort: Optional[str] = "date_desc"
):
    db = get_db()
    query = """
        SELECT se.*, e.last_name || ' ' || e.first_name || COALESCE(' ' || e.middle_name, '') as employee_name,
               u.full_name as created_by_name
        FROM staff_events se
        JOIN employees e ON se.employee_id = e.id
        LEFT JOIN users u ON se.created_by = u.id
        WHERE 1=1
    """
    params = []

    if employee_id:
        query += " AND se.employee_id = ?"
        params.append(employee_id)

    if event_type:
        query += " AND se.event_type = ?"
        params.append(event_type)

    sort_map = {
        "date_desc": "se.event_date DESC",
        "date_asc": "se.event_date ASC",
        "type": "se.event_type ASC",
    }
    query += f" ORDER BY {sort_map.get(sort, 'se.event_date DESC')}"

    rows = db.execute(query, params).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.post("")
def create_event(data: StaffEventCreate):
    db = get_db()
    cursor = db.execute("""
        INSERT INTO staff_events (employee_id, event_type, event_date, end_date, description, document_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.employee_id, data.event_type, data.event_date, data.end_date, data.description, data.document_number))
    db.commit()
    event_id = cursor.lastrowid

    # Update employee status based on event type
    status_map = {
        "приём": "работает",
        "увольнение": "уволен",
        "отпуск": "в отпуске",
        "больничный": "больничный",
        "командировка": "командировка",
    }
    if data.event_type in status_map:
        db.execute("UPDATE employees SET status = ? WHERE id = ?", (status_map[data.event_type], data.employee_id))
        db.commit()

    db.close()
    return {"id": event_id, "message": "Кадровое событие создано"}


@router.delete("/{event_id}")
def delete_event(event_id: int):
    db = get_db()
    db.execute("DELETE FROM staff_events WHERE id = ?", (event_id,))
    db.commit()
    db.close()
    return {"message": "Кадровое событие удалено"}
