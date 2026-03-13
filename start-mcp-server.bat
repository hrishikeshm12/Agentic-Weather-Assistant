@echo off
REM Start MCP Server only

cd /d "%~dp0"

if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo Starting MCP Server on port 8001...
echo MCP Server URL: http://localhost:8001
echo.

.\venv\Scripts\python mcp-server\server.py

pause
