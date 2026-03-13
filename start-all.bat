@echo off
REM Start all services for the Weather Agent Application
setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo      WEATHER AGENT - STARTING ALL SERVICES
echo ================================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo.
    pause
    exit /b 1
)

echo Launching 3 terminal windows...
echo.

REM Start MCP Server
echo [1/3] Starting MCP Server on port 8001...
start "MCP Server - Weather API Wrapper" cmd /k "title MCP Server (8001) && cd /d %cd% && .\venv\Scripts\python mcp-server\server.py"
timeout /t 2 /nobreak

REM Start Backend Agent
echo [2/3] Starting Backend Agent on port 8000...
start "Backend Agent - Claude AI" cmd /k "title Backend Agent (8000) && cd /d %cd% && .\venv\Scripts\python backend\app.py"
timeout /t 2 /nobreak

REM Start Frontend
echo [3/3] Starting Frontend on port 8002...
start "Frontend - Chat UI" cmd /k "title Frontend (8002) && cd /d %cd%\frontend && python -m http.server 8002"
timeout /t 2 /nobreak

cls
echo.
echo ================================================
echo         ALL SERVICES STARTED SUCCESSFULLY!
echo ================================================
echo.
echo Three new windows should have opened:
echo   1. MCP Server (8001)     - Weather API wrapper
echo   2. Backend Agent (8000)  - Claude AI + Tool calling
echo   3. Frontend (8002)       - Chat interface
echo.
echo NEXT STEPS:
echo   1. Open browser: http://localhost:8002
echo   2. Ask: "What's the weather in London?"
echo   3. Watch the logs in each window!
echo.
echo PORTS:
echo   MCP Server:     http://localhost:8001
echo   Backend Agent:  http://localhost:8000
echo   Frontend:       http://localhost:8002
echo.
echo Press any key to close this window...
pause>nul

