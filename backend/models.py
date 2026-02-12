from pydantic import BaseModel
from typing import Optional
from datetime import date


# --- Auth ---
class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    full_name: str
    role_id: Optional[int] = 2


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role_id: int
    role_name: Optional[str] = None
    is_active: int
    created_at: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[int] = None


# --- Department ---
class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    head_name: Optional[str] = None
    phone: Optional[str] = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    head_name: Optional[str] = None
    phone: Optional[str] = None
    employee_count: Optional[int] = 0


# --- Position ---
class PositionCreate(BaseModel):
    name: str
    department_id: Optional[int] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    description: Optional[str] = None


class PositionOut(BaseModel):
    id: int
    name: str
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    description: Optional[str] = None


# --- Employee ---
class EmployeeCreate(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    hire_date: str
    salary: Optional[float] = None
    employment_type: Optional[str] = "штатный"
    status: Optional[str] = "работает"
    photo_url: Optional[str] = None


class EmployeeOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    position_id: Optional[int] = None
    position_name: Optional[str] = None
    hire_date: str
    salary: Optional[float] = None
    employment_type: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: Optional[str] = None
    full_name: Optional[str] = None


# --- Contact ---
class ContactCreate(BaseModel):
    employee_id: int
    contact_type: str
    contact_value: str
    is_primary: Optional[int] = 0


class ContactOut(BaseModel):
    id: int
    employee_id: int
    contact_type: str
    contact_value: str
    is_primary: int


# --- Education ---
class EducationCreate(BaseModel):
    employee_id: int
    institution: str
    speciality: Optional[str] = None
    degree: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    diploma_number: Optional[str] = None


class EducationOut(BaseModel):
    id: int
    employee_id: int
    institution: str
    speciality: Optional[str] = None
    degree: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    diploma_number: Optional[str] = None


# --- Staff Event ---
class StaffEventCreate(BaseModel):
    employee_id: int
    event_type: str
    event_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    document_number: Optional[str] = None


class StaffEventOut(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    event_type: str
    event_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    document_number: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[str] = None
