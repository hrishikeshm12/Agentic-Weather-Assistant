@echo off
REM Start all servers for the weather agent application

echo.
echo ==========================================
echo Weather Agent Application - Starting Services
echo ==========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Missing virtual environment. Run: python -m venv venv
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

echo.
echo Virtual environment activated
echo.

REM Start MCP Server in a new window
echo Starting MCP Server on port 8001...
start "MCP Server" cmd /k "cd mcp-server && python server.py"
timeout /t 2 /nobreak

echo.

REM Start Backend Agent in a new window
echo Starting Backend Agent on port 8000...
start "Backend Agent" cmd /k "cd backend && python app.py"
timeout /t 2 /nobreak

echo.

REM Display startup info
echo.
echo ==========================================
echo Services Started Successfully!
echo ==========================================
echo.
echo Available endpoints:
echo   - Backend Agent:  http://localhost:8000
echo   - MCP Server:     http://localhost:8001
echo   - Frontend:       Open frontend/index.html in your browser
echo.
echo To test the agent, open PowerShell and run:
echo   curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"query\": \"What is the weather in London?\"}"
echo.
echo All servers are running in separate windows.
echo Close windows to stop services.
echo.
pause
