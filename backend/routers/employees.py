from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import get_db
from models import EmployeeCreate, EmployeeOut, ContactCreate, ContactOut, EducationCreate, EducationOut

router = APIRouter()


@router.get("")
def get_employees(
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    employment_type: Optional[str] = None,
    sort: Optional[str] = "last_name"
):
    db = get_db()
    query = """
        SELECT e.*, d.name as department_name, p.name as position_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (LOWER(e.last_name) LIKE LOWER(?) OR LOWER(e.first_name) LIKE LOWER(?) OR LOWER(e.middle_name) LIKE LOWER(?) OR e.phone LIKE ? OR LOWER(e.email) LIKE LOWER(?))"
        s = f"%{search}%"
        params.extend([s, s, s, s, s])

    if department_id:
        query += " AND e.department_id = ?"
        params.append(department_id)

    if status:
        query += " AND e.status = ?"
        params.append(status)

    if employment_type:
        query += " AND e.employment_type = ?"
        params.append(employment_type)

    sort_map = {
        "last_name": "e.last_name ASC",
        "hire_date": "e.hire_date DESC",
        "salary": "e.salary DESC",
        "department": "d.name ASC",
    }
    query += f" ORDER BY {sort_map.get(sort, 'e.last_name ASC')}"

    rows = db.execute(query, params).fetchall()
    result = []
    for r in rows:
        emp = dict(r)
        emp["full_name"] = f"{emp['last_name']} {emp['first_name']}" + (f" {emp['middle_name']}" if emp.get('middle_name') else "")
        result.append(emp)
    db.close()
    return result


@router.get("/{employee_id}")
def get_employee(employee_id: int):
    db = get_db()
    row = db.execute("""
        SELECT e.*, d.name as department_name, p.name as position_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE e.id = ?
    """, (employee_id,)).fetchone()

    if not row:
        db.close()
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    emp = dict(row)
    emp["full_name"] = f"{emp['last_name']} {emp['first_name']}" + (f" {emp['middle_name']}" if emp.get('middle_name') else "")

    contacts = db.execute("SELECT * FROM contacts WHERE employee_id = ?", (employee_id,)).fetchall()
    emp["contacts"] = [dict(c) for c in contacts]

    education = db.execute("SELECT * FROM education WHERE employee_id = ?", (employee_id,)).fetchall()
    emp["education"] = [dict(e) for e in education]

    events = db.execute("""
        SELECT se.*, u.full_name as created_by_name
        FROM staff_events se
        LEFT JOIN users u ON se.created_by = u.id
        WHERE se.employee_id = ?
        ORDER BY se.event_date DESC
    """, (employee_id,)).fetchall()
    emp["events"] = [dict(ev) for ev in events]

    db.close()
    return emp


@router.post("")
def create_employee(data: EmployeeCreate):
    db = get_db()
    cursor = db.execute("""
        INSERT INTO employees (last_name, first_name, middle_name, birth_date, gender, inn, snils,
            passport_series, passport_number, address, phone, email, department_id, position_id,
            hire_date, salary, employment_type, status, photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data.last_name, data.first_name, data.middle_name, data.birth_date, data.gender,
          data.inn, data.snils, data.passport_series, data.passport_number, data.address,
          data.phone, data.email, data.department_id, data.position_id, data.hire_date,
          data.salary, data.employment_type, data.status, data.photo_url))
    db.commit()
    emp_id = cursor.lastrowid
    db.close()
    return {"id": emp_id, "message": "Сотрудник добавлен"}


@router.put("/{employee_id}")
def update_employee(employee_id: int, data: EmployeeCreate):
    db = get_db()
    db.execute("""
        UPDATE employees SET last_name=?, first_name=?, middle_name=?, birth_date=?, gender=?,
            inn=?, snils=?, passport_series=?, passport_number=?, address=?, phone=?, email=?,
            department_id=?, position_id=?, hire_date=?, salary=?, employment_type=?, status=?, photo_url=?
        WHERE id=?
    """, (data.last_name, data.first_name, data.middle_name, data.birth_date, data.gender,
          data.inn, data.snils, data.passport_series, data.passport_number, data.address,
          data.phone, data.email, data.department_id, data.position_id, data.hire_date,
          data.salary, data.employment_type, data.status, data.photo_url, employee_id))
    db.commit()
    db.close()
    return {"message": "Данные сотрудника обновлены"}


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    db = get_db()
    db.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    db.commit()
    db.close()
    return {"message": "Сотрудник удалён"}


# --- Contacts ---
@router.get("/{employee_id}/contacts")
def get_contacts(employee_id: int):
    db = get_db()
    rows = db.execute("SELECT * FROM contacts WHERE employee_id = ?", (employee_id,)).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.post("/{employee_id}/contacts")
def add_contact(employee_id: int, data: ContactCreate):
    db = get_db()
    data.employee_id = employee_id
    db.execute("INSERT INTO contacts (employee_id, contact_type, contact_value, is_primary) VALUES (?, ?, ?, ?)",
               (employee_id, data.contact_type, data.contact_value, data.is_primary))
    db.commit()
    db.close()
    return {"message": "Контакт добавлен"}


@router.delete("/{employee_id}/contacts/{contact_id}")
def delete_contact(employee_id: int, contact_id: int):
    db = get_db()
    db.execute("DELETE FROM contacts WHERE id = ? AND employee_id = ?", (contact_id, employee_id))
    db.commit()
    db.close()
    return {"message": "Контакт удалён"}


# --- Education ---
@router.get("/{employee_id}/education")
def get_education(employee_id: int):
    db = get_db()
    rows = db.execute("SELECT * FROM education WHERE employee_id = ?", (employee_id,)).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.post("/{employee_id}/education")
def add_education(employee_id: int, data: EducationCreate):
    db = get_db()
    data.employee_id = employee_id
    db.execute("""INSERT INTO education (employee_id, institution, speciality, degree, year_start, year_end, diploma_number)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
               (employee_id, data.institution, data.speciality, data.degree, data.year_start, data.year_end, data.diploma_number))
    db.commit()
    db.close()
    return {"message": "Образование добавлено"}


@router.delete("/{employee_id}/education/{edu_id}")
def delete_education(employee_id: int, edu_id: int):
    db = get_db()
    db.execute("DELETE FROM education WHERE id = ? AND employee_id = ?", (edu_id, employee_id))
    db.commit()
    db.close()
    return {"message": "Запись об образовании удалена"}
