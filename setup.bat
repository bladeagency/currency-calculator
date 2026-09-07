@echo off
setlocal enabledelayedexpansion

echo === Currency Calculator Setup ===

:: Переходим в папку, где лежит этот bat-файл
cd /d "%~dp0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

:: Создаём виртуальное окружение, если его нет
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create venv.
        pause
        exit /b 1
    )
)

echo Activating venv...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies. Please check your internet connection.
    pause
    exit /b 1
)

echo Starting server...
echo Server will be available at http://localhost:8000
echo Press Ctrl+C to stop.
uvicorn src.main:app --host 127.0.0.1 --port 8080 --reload

pause