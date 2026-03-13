# 🚀 Quick Start Guide

## Project Status
✅ Virtual environment setup complete
✅ All dependencies installed
✅ API keys configured
✅ Ready to run!

## Python Version
- Recommended: Python `3.11`
- Supported: Python `3.10` to `3.13`
- Not supported for current dependency set: Python `3.14+`

## Running the Application

### Windows Users

**Option 1: Automatic (Recommended)**
```bash
start-servers.bat
```
This will start both the MCP Server and Backend Agent in separate terminal windows.

**Option 2: Manual (Terminal)**
```bash
# Terminal 1: Start MCP Server (port 8001)
cd mcp-server
..\venv\Scripts\python.exe server.py

# Terminal 2: Start Backend Agent (port 8000)
cd backend
..\venv\Scripts\python.exe app.py

# Terminal 3: Open Frontend
# Open frontend/index.html in your browser
```

### Linux/Mac Users

```bash
bash start-servers.sh
```

## Access the Application

1. **Frontend**: Open `http://localhost:8000` in your browser
2. **API Documentation**: `http://localhost:8000` shows all endpoints
3. **Try a Query**: Ask "What's the weather in London?"

## Testing the API

### Test Backend Agent
```powershell
curl -X POST http://localhost:8000/query `
  -H "Content-Type: application/json" `
  -d '{"query": "What is the weather in New York?"}'
```

### Test MCP Server
```powershell
curl http://localhost:8001/tools
```

### Check Health
```powershell
# Backend
curl http://localhost:8000/health

# MCP Server
curl http://localhost:8001/health
```

## API Endpoints

### Backend Agent (Port 8000)
- `GET /health` - Health check
- `POST /query` - Query the weather agent
- `GET /examples` - Get example queries
- `GET /` - Service info

### MCP Server (Port 8001)
- `GET /health` - Health check
- `GET /tools` - List available tools
- `POST /call` - Call a tool (JSON-RPC 2.0)
- `GET /` - Service info

## File Structure
```
D:\Inmarket\
├── .env                    # Configuration (with API keys)
├── venv/                   # Python virtual environment
├── frontend/               # Web UI files
├── backend/                # Flask agent server
├── mcp-server/             # Weather API wrapper
├── start-servers.bat       # Windows startup script
├── start-servers.sh        # Linux/Mac startup script
└── README.md               # Full documentation
```

## Troubleshooting

### Port Already in Use
```bash
# Windows - Find and kill process on port 8000/8001
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Missing Dependencies
```bash
# Reinstall in venv
.\venv\Scripts\pip.exe install -r requirements.txt
```

### API Key Issues
```bash
# Check .env file has valid keys:
cat .env | grep "API_KEY"
```

## Key Technologies

- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Backend**: Flask + LangChain + Claude API
- **MCP Server**: Flask + JSON-RPC 2.0 + OpenWeather API
- **Python Version**: 3.10+

## Environment Variables

```
OPENWEATHER_API_KEY=...     # Free API key from OpenWeather
ANTHROPIC_API_KEY=...       # Claude API key
FLASK_ENV=development       # Flask environment
MCP_SERVER_PORT=8001        # MCP Server port
BACKEND_PORT=8000           # Backend server port
MCP_SERVER_URL=...          # URL for MCP Server
```

## Next Steps

1. **Start the servers** using the commands above
2. **Test the frontend** at http://localhost:8000
3. **Ask questions** like:
   - "What's the weather in Tokyo?"
   - "Will it rain in London tomorrow?"
   - "Compare weather in Paris and Barcelona"
4. **Review code** in each component for how it works
5. **Prepare video demo** showing:
   - Your development approach
   - Key prompts used in the agentic IDE
   - Live demo of queries
   - Architecture explanation
   - Deployment discussion

## Support

Check `README.md` for detailed documentation on:
- Architecture overview
- API reference
- Design decisions
- Deployment options
- Troubleshooting guide
