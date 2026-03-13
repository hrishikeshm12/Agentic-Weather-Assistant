@echo off
REM Start Frontend Server only

cd /d "%~dp0\frontend"

echo Starting Frontend on port 8002...
echo Frontend URL: http://localhost:8002
echo Make sure Backend is running on http://localhost:8000
echo.

python -m http.server 8002

pause
