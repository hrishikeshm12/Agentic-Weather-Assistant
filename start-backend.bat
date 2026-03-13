@echo off
REM Start Backend Agent Server only

cd /d "%~dp0"

if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo Starting Backend Agent on port 8000...
echo Backend URL: http://localhost:8000
echo Make sure MCP Server is running on http://localhost:8001
echo.

.\venv\Scripts\python backend\app.py

pause
