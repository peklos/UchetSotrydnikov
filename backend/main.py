from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

from database import init_db
from seed_data import seed_all
from routers import auth, employees, departments, positions, staff_events, reports, admin

app = FastAPI(title="Учёт сотрудников — ГАУК «Брянская областная филармония»")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Авторизация"])
app.include_router(employees.router, prefix="/api/employees", tags=["Сотрудники"])
app.include_router(departments.router, prefix="/api/departments", tags=["Подразделения"])
app.include_router(positions.router, prefix="/api/positions", tags=["Должности"])
app.include_router(staff_events.router, prefix="/api/events", tags=["Кадровые события"])
app.include_router(reports.router, prefix="/api/reports", tags=["Отчёты"])
app.include_router(admin.router, prefix="/api/admin", tags=["Админка"])

# Serve frontend static files
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


@app.on_event("startup")
def startup():
    init_db()
    seed_all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
