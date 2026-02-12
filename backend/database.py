import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "philharmonic.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role_id INTEGER NOT NULL DEFAULT 2,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        );

        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            head_name TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary_min REAL,
            salary_max REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            birth_date TEXT,
            gender TEXT CHECK(gender IN ('М', 'Ж')),
            inn TEXT,
            snils TEXT,
            passport_series TEXT,
            passport_number TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            department_id INTEGER,
            position_id INTEGER,
            hire_date TEXT NOT NULL,
            salary REAL,
            employment_type TEXT DEFAULT 'штатный' CHECK(employment_type IN ('штатный', 'совместитель', 'срочный договор', 'ГПД')),
            status TEXT DEFAULT 'работает' CHECK(status IN ('работает', 'в отпуске', 'больничный', 'уволен', 'командировка')),
            photo_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
            FOREIGN KEY (position_id) REFERENCES positions(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            contact_type TEXT NOT NULL CHECK(contact_type IN ('телефон', 'email', 'telegram', 'другое')),
            contact_value TEXT NOT NULL,
            is_primary INTEGER DEFAULT 0,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            institution TEXT NOT NULL,
            speciality TEXT,
            degree TEXT CHECK(degree IN ('среднее', 'среднее специальное', 'бакалавр', 'магистр', 'специалист', 'аспирант', 'кандидат наук', 'доктор наук')),
            year_start INTEGER,
            year_end INTEGER,
            diploma_number TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS staff_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            event_type TEXT NOT NULL CHECK(event_type IN ('приём', 'увольнение', 'перевод', 'отпуск', 'больничный', 'командировка', 'повышение', 'выговор', 'премия')),
            event_date TEXT NOT NULL,
            end_date TEXT,
            description TEXT,
            document_number TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
        );
    """)

    conn.commit()
    conn.close()
