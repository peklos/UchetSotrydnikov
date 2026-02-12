@echo off
chcp 65001 >nul
echo ========================================
echo   Режим разработки (dev)
echo ========================================
echo.

:: Install deps
cd backend
pip install -r requirements.txt -q
cd ..\frontend
call npm install --silent
cd ..

:: Start backend in background
echo Запуск backend на http://127.0.0.1:8000 ...
start "Backend" cmd /c "cd backend && python main.py"

:: Wait a moment for backend to start
timeout /t 2 /nobreak >nul

:: Start frontend dev server
echo Запуск frontend на http://127.0.0.1:5173 ...
cd frontend
call npm run dev
