from fastapi import APIRouter
from database import get_db

router = APIRouter()


@router.get("/stats")
def get_stats():
    db = get_db()

    total = db.execute("SELECT COUNT(*) as cnt FROM employees WHERE status != 'уволен'").fetchone()["cnt"]
    fired = db.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'уволен'").fetchone()["cnt"]
    on_vacation = db.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'в отпуске'").fetchone()["cnt"]
    on_sick = db.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'больничный'").fetchone()["cnt"]
    on_trip = db.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'командировка'").fetchone()["cnt"]
    dept_count = db.execute("SELECT COUNT(*) as cnt FROM departments").fetchone()["cnt"]
    pos_count = db.execute("SELECT COUNT(*) as cnt FROM positions").fetchone()["cnt"]

    avg_salary = db.execute("SELECT AVG(salary) as avg_sal FROM employees WHERE status != 'уволен' AND salary > 0").fetchone()["avg_sal"]

    db.close()
    return {
        "total_employees": total,
        "fired_employees": fired,
        "on_vacation": on_vacation,
        "on_sick_leave": on_sick,
        "on_business_trip": on_trip,
        "departments_count": dept_count,
        "positions_count": pos_count,
        "average_salary": round(avg_salary, 2) if avg_salary else 0,
    }


@router.get("/by-department")
def by_department():
    db = get_db()
    rows = db.execute("""
        SELECT d.name, COUNT(e.id) as employee_count, AVG(e.salary) as avg_salary
        FROM departments d
        LEFT JOIN employees e ON e.department_id = d.id AND e.status != 'уволен'
        GROUP BY d.id
        ORDER BY employee_count DESC
    """).fetchall()
    db.close()
    return [{"name": r["name"], "employee_count": r["employee_count"], "avg_salary": round(r["avg_salary"] or 0, 2)} for r in rows]


@router.get("/by-status")
def by_status():
    db = get_db()
    rows = db.execute("""
        SELECT status, COUNT(*) as count FROM employees GROUP BY status ORDER BY count DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/by-employment-type")
def by_employment_type():
    db = get_db()
    rows = db.execute("""
        SELECT employment_type, COUNT(*) as count FROM employees WHERE status != 'уволен' GROUP BY employment_type ORDER BY count DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/by-gender")
def by_gender():
    db = get_db()
    rows = db.execute("""
        SELECT gender, COUNT(*) as count FROM employees WHERE status != 'уволен' AND gender IS NOT NULL GROUP BY gender
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/recent-events")
def recent_events():
    db = get_db()
    rows = db.execute("""
        SELECT se.*, e.last_name || ' ' || e.first_name as employee_name
        FROM staff_events se
        JOIN employees e ON se.employee_id = e.id
        ORDER BY se.created_at DESC
        LIMIT 20
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/staffing")
def staffing_table():
    """Штатное расписание"""
    db = get_db()
    rows = db.execute("""
        SELECT d.name as department_name, p.name as position_name,
               p.salary_min, p.salary_max,
               COUNT(e.id) as filled,
               GROUP_CONCAT(e.last_name || ' ' || e.first_name, ', ') as employees
        FROM positions p
        LEFT JOIN departments d ON p.department_id = d.id
        LEFT JOIN employees e ON e.position_id = p.id AND e.status != 'уволен'
        GROUP BY p.id
        ORDER BY d.name, p.name
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@router.get("/vacation-schedule")
def vacation_schedule():
    """График отпусков"""
    db = get_db()
    rows = db.execute("""
        SELECT se.event_date, se.end_date, se.description,
               e.last_name || ' ' || e.first_name || COALESCE(' ' || e.middle_name, '') as employee_name,
               d.name as department_name, p.name as position_name
        FROM staff_events se
        JOIN employees e ON se.employee_id = e.id
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE se.event_type = 'отпуск'
        ORDER BY se.event_date DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]
