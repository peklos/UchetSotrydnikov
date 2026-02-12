@echo off
chcp 65001 >nul
echo ========================================
echo   Учёт сотрудников — Запуск системы
echo   ГАУК «Брянская областная филармония»
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден! Установите Python 3.9+ с python.org
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Node.js не найден! Установите Node.js 18+ с nodejs.org
    pause
    exit /b 1
)

:: Install backend dependencies
echo [1/4] Установка зависимостей backend...
cd backend
pip install -r requirements.txt -q
cd ..

:: Install frontend dependencies
echo [2/4] Установка зависимостей frontend...
cd frontend
call npm install --silent
echo [3/4] Сборка frontend...
call npm run build
cd ..

:: Start backend
echo [4/4] Запуск сервера...
echo.
echo Сервер запущен на http://127.0.0.1:8000
echo Нажмите Ctrl+C для остановки
echo.
cd backend
python main.py
