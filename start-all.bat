@echo off
REM Start all services for the Weather Agent Application

echo ========================================
echo Weather Agent - Starting All Services
echo ========================================

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Create new terminal windows for each service
echo Starting MCP Server on port 8001...
start "MCP Server" cmd /k "cd /d %cd% && .\venv\Scripts\python mcp-server\server.py"

timeout /t 2

echo Starting Backend Agent on port 8000...
start "Backend Agent" cmd /k "cd /d %cd% && .\venv\Scripts\python backend\app.py"

timeout /t 2

echo Starting Frontend on port 8002...
start "Frontend" cmd /k "cd /d %cd%\frontend && python -m http.server 8002"

timeout /t 3

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo MCP Server:     http://localhost:8001
echo Backend Agent:  http://localhost:8000
echo Frontend:       http://localhost:8002
echo.
echo Open your browser to: http://localhost:8002
echo.
pause
