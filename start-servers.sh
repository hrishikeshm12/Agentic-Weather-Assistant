#!/bin/bash
# Start all servers for the weather agent application

cd "$(dirname "$0")"

echo "=========================================="
echo "Weather Agent Application - Starting Services"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate venv
source venv/Scripts/activate 2>/dev/null || . venv/Scripts/activate

echo "✓ Virtual environment activated"
echo ""

# Start MCP Server
echo "Starting MCP Server on port 8001..."
cd mcp-server
python server.py &
MCP_PID=$!
echo "✓ MCP Server started (PID: $MCP_PID)"
cd ..
sleep 2

echo ""

# Start Backend Agent
echo "Starting Backend Agent on port 8000..."
cd backend
python app.py &
BACKEND_PID=$!
echo "✓ Backend Agent started (PID: $BACKEND_PID)"
cd ..
sleep 2

echo ""

# Frontend info
echo "=========================================="
echo "✓ Services Started Successfully!"
echo "=========================================="
echo ""
echo "Available endpoints:"
echo "  - Backend Agent:  http://localhost:8000"
echo "  - MCP Server:     http://localhost:8001"
echo "  - Frontend:       Open frontend/index.html in your browser"
echo ""
echo "Query the agent:"
echo "  curl -X POST http://localhost:8000/query \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"query\": \"What is the weather in London?\"}'"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait
