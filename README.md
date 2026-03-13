# AI Builder Project: Agentic Weather Assistant

An end-to-end agentic application that combines OpenWeather API integration, an MCP Server wrapper, and LangChain-powered LLM agents to provide intelligent weather insights.

## Architecture Overview

```
┌─────────────────┐
│   Frontend App  │
│  (React/HTML)   │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────────────┐
│  Backend Agent Server   │
│  (Flask + LangChain)    │
└────────┬────────────────┘
         │ JSON-RPC
         ↓
┌─────────────────────────┐
│   MCP Server Wrapper    │
│  (OpenWeather API)      │
└────────┬────────────────┘
         │ HTTP
         ↓
┌─────────────────────────┐
│   OpenWeather API       │
│   (Third-party Service) │
└─────────────────────────┘
```

## Components

### 1. MCP Server (`/mcp-server`)
- Wraps OpenWeather API calls
- Exposes tools: `get_current_weather`, `get_forecast`, `search_cities`
- Implements JSON-RPC 2.0 protocol
- Handles API key management securely

### 2. Backend Agent (`/backend`)
- Flask HTTP server
- LangChain integration for tool calling
- Claude API integration for intelligent responses
- Prompt engineering for contextual weather analysis

### 3. Frontend (`/frontend`)
- Simple HTML/CSS/JavaScript interface
- Real-time chat interaction
- Display weather data with AI insights
- Responsive design

## Setup & Installation

### Prerequisites
- Python 3.10 to 3.13 (3.11 recommended; 3.14+ is not supported by current LangChain/Pydantic dependencies)
- Node.js 16+ (for frontend)
- OpenWeather API key (free tier: https://openweathermap.org/api)
- Anthropic Claude API key (https://console.anthropic.com)

### Step 1: Environment Setup

```bash
# Create .env file in project root
cat > .env << 'EOF'
OPENWEATHER_API_KEY=your_openweather_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
FLASK_ENV=development
MCP_SERVER_PORT=8001
BACKEND_PORT=8000
EOF
```

### Step 2: Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# MCP Server dependencies
cd mcp-server
pip install -r requirements.txt
cd ..

# Frontend dependencies (optional, if using Node)
cd frontend
npm install
cd ..
```

### Step 3: Run the Application

**Terminal 1: Start MCP Server**
```bash
cd mcp-server
python server.py
# Server runs on http://localhost:8001
```

**Terminal 2: Start Backend Agent**
```bash
cd backend
python app.py
# Server runs on http://localhost:8000
```

**Terminal 3: Run Frontend**
```bash
cd frontend
# Option A: Open index.html in browser (if static)
# Option B: If using Node
npm run dev
```

Then open your browser to `http://localhost:8000` (or port shown in frontend output).

## Usage

1. Open the web app in your browser
2. Ask the agent about weather in any city:
   - "What's the weather in New York?"
   - "Will it rain in London tomorrow?"
   - "Compare weather in Tokyo and Sydney"
3. The agent will:
   - Use the MCP Server tools to fetch weather data
   - Analyze the data using Claude
   - Provide intelligent, contextual responses

## API Reference

### MCP Server Tools

#### `get_current_weather`
Returns current weather for a city.
```json
{
  "city": "string",
  "country": "string",
  "temperature": "number (Celsius)",
  "condition": "string",
  "humidity": "number",
  "wind_speed": "number",
  "description": "string"
}
```

#### `get_forecast`
Returns 5-day weather forecast.
```json
{
  "city": "string",
  "forecasts": [
    {
      "date": "YYYY-MM-DD",
      "temp_max": "number",
      "temp_min": "number",
      "condition": "string"
    }
  ]
}
```

#### `search_cities`
Searches for cities by name.
```json
{
  "results": [
    {
      "name": "string",
      "country": "string",
      "latitude": "number",
      "longitude": "number"
    }
  ]
}
```

## Key Design Decisions

### MCP Server Architecture
- **Separation of Concerns**: MCP Server handles only API integration, no business logic
- **Security**: API keys stored in environment variables, never exposed to frontend
- **Extensibility**: Easy to add new weather data providers

### LLM Agent Design
- **Tool Definitions**: Clear, descriptive tool schemas for LangChain
- **Prompt Engineering**: System prompt guides agent to provide contextual weather analysis
- **Error Handling**: Graceful fallbacks when tools fail or data is unavailable

### Frontend Design
- **Simple & Focused**: Clean UI focused on core functionality
- **Responsive**: Works on desktop and mobile
- **Real-time**: Chat-like interface for natural interaction

## Deployment Considerations

### Docker Containerization
```bash
docker-compose up
```
Services run in isolated containers with proper networking.

### Kubernetes
- Create separate deployments for each service
- Use ConfigMaps for environment configuration
- Use Secrets for API keys

### Serverless (AWS Lambda/Google Cloud Functions)
- MCP Server: Deploy as Cloud Function or Lambda
- Backend Agent: Deploy as Lambda/Cloud Function
- Frontend: Host on S3/Cloud Storage with CDN

## Documentation Philosophy

### For Collaborating Developers
- Clear README with setup instructions
- Code comments for complex logic
- Architecture diagrams in documentation
- Example API requests/responses

### For New Team Members
- Step-by-step setup guide
- Architecture overview with diagrams
- Individual component documentation
- Common troubleshooting guide

## Development Notes

### Adding New Weather Tools
1. Add tool function to MCP Server
2. Export from `tools.py`
3. Register in LangChain backend
4. Test with agent

### Debugging
```bash
# Enable verbose logging
export DEBUG=True

# Check MCP Server logs
curl http://localhost:8001/health

# Test backend agent directly
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in London?"}'
```

## File Structure

```
inmarket-agentic-weather/
├── README.md                 # This file
├── .env                      # Environment variables (git-ignored)
├── requirements.txt          # Python dependencies
│
├── mcp-server/
│   ├── requirements.txt
│   ├── server.py            # Main MCP Server
│   ├── tools.py             # Weather API tools
│   └── config.py            # Configuration
│
├── backend/
│   ├── requirements.txt
│   ├── app.py               # Flask application
│   ├── agent.py             # LangChain agent setup
│   ├── prompts.py           # Prompt templates
│   └── config.py            # Configuration
│
└── frontend/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Troubleshooting

**MCP Server won't start**
- Check if port 8001 is available: `netstat -an | grep 8001`
- Verify OPENWEATHER_API_KEY is set: `echo $OPENWEATHER_API_KEY`

**Backend agent returns errors**
- Verify MCP Server is running and accessible
- Check ANTHROPIC_API_KEY is valid
- Review backend logs for detailed error messages

**Frontend can't connect to backend**
- Check backend is running on correct port
- Verify CORS headers in Flask app
- Check browser console for network errors

## License

MIT

## Contact

InMarket AI Builder Interview Project
