# AI Builder Project: Agentic Weather Assistant

An end-to-end agentic application that combines OpenWeather API integration, an MCP Server wrapper, and Claude AI with native tool use for intelligent weather insights.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                           │
│                    http://localhost:8002                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP (REST)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 BACKEND AGENT SERVER (Flask)                    │
│                    http://localhost:8000                        │
│                                                                 │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │ Conversation │  │  Claude API     │  │  Prompt          │    │
│  │ History      │  │  (Tool Use)     │  │  Engineering     │    │
│  │ Management   │  │  Agentic Loop   │  │  System Prompt   │    │
│  └──────────────┘  └────────┬────────┘  └──────────────────┘    │
└─────────────────────────────┼───────────────────────────────────┘
                              │ JSON-RPC 2.0
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP SERVER (Flask)                           │
│                    http://localhost:8001                        │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ get_current_     │  │ get_forecast │  │ search_cities   │    │
│  │ weather          │  │              │  │                 │    │
│  └────────┬─────────┘  └──────┬───────┘  └────────┬───────┘     │
└───────────┼───────────────────┼────────────────────┼────────────┘
            │                   │                    │
            └───────────────────┼────────────────────┘
                                │ HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenWeather API                              │
│              api.openweathermap.org (External)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

- **Agentic AI**: Claude autonomously decides which tools to call, processes results, and synthesizes natural language responses
- **Multi-turn Conversations**: Agent maintains conversation history for contextual follow-up questions
- **Tool Call Transparency**: Frontend displays which MCP tools the agent called and their results
- **MCP Architecture**: Clean separation between API wrapper (MCP Server) and AI reasoning (Backend Agent)
- **JSON-RPC 2.0**: Standard protocol for tool invocation between Backend and MCP Server

## Components

### 1. MCP Server (`/mcp-server`)
- Wraps OpenWeather API calls into standardized tools
- Exposes tools: `get_current_weather`, `get_forecast`, `search_cities`
- Implements JSON-RPC 2.0 protocol for tool calling
- Handles API key management securely (never exposed to frontend)

### 2. Backend Agent (`/backend`)
- Flask HTTP server with CORS support
- Claude API with native tool use (agentic loop pattern)
- Conversation history for multi-turn interactions
- Tool call metadata returned to frontend for transparency
- Prompt engineering for contextual weather analysis

### 3. Frontend (`/frontend`)
- Vanilla HTML/CSS/JavaScript chat interface
- Displays agent tool calls in real-time (agent transparency)
- Markdown rendering with XSS prevention
- "New Chat" button to reset conversation context
- Responsive design for desktop and mobile

## Setup & Installation

### Prerequisites
- Python 3.10+
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
MCP_SERVER_URL=http://localhost:8001
EOF
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

**Windows (Recommended):**
```bash
# Simply double-click or run:
start-all.bat
```

This opens three terminal windows, one for each service.

**Manual (All Platforms):**

```bash
# Terminal 1: MCP Server
python mcp-server/server.py       # http://localhost:8001

# Terminal 2: Backend Agent
python backend/app.py             # http://localhost:8000

# Terminal 3: Frontend
cd frontend && python -m http.server 8002   # http://localhost:8002
```

Then open your browser to `http://localhost:8002`.

## Usage

1. Open `http://localhost:8002` in your browser
2. Ask the agent about weather in any city:
   - "What's the weather in New York?"
   - "Will it rain in London tomorrow?"
   - "Compare weather in Tokyo and Sydney"
3. The agent will:
   - Autonomously select and call MCP tools
   - Display which tools were called (visible in the chat)
   - Provide intelligent, contextual responses
4. Ask follow-up questions - the agent remembers conversation context
5. Click "New Chat" to start a fresh conversation

## How the Agentic Loop Works

```
User Query → Claude API (with tool definitions)
                    │
                    ├── Claude decides to call tools → MCP Server → OpenWeather API
                    │                                      │
                    │   ← Tool results returned ───────────┘
                    │
                    ├── Claude may call more tools (multi-step reasoning)
                    │
                    └── Claude generates final natural language response → User
```

The agent can make multiple tool calls per query (e.g., fetching weather for two cities to compare them), and the loop continues until Claude decides it has enough information to respond.

## API Reference

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/query` | POST | Send a query to the agent |
| `/examples` | GET | Get example queries |
| `/reset` | POST | Clear conversation history |

### MCP Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/tools` | GET | List available tools |
| `/call` | POST | Call a tool (JSON-RPC 2.0) |

### MCP Tools

- **get_current_weather(city, country?)** - Current conditions (temp, humidity, wind, etc.)
- **get_forecast(city, country?, days?)** - 5-day forecast with daily highs/lows
- **search_cities(query, limit?)** - Search cities by name with coordinates

## Key Design Decisions

### MCP Server Architecture
- **Separation of Concerns**: MCP Server handles only API integration, no business logic
- **Protocol**: JSON-RPC 2.0 for standardized tool invocation
- **Security**: API keys stored in environment variables, never exposed to frontend
- **Extensibility**: Easy to add new weather data providers or tools

### LLM Agent Design
- **Native Tool Use**: Uses Claude's built-in tool_use feature (not framework wrappers)
- **Agentic Loop**: Handles multi-step reasoning with up to 10 iterations
- **Conversation Memory**: Maintains history for contextual follow-ups
- **Prompt Engineering**: System prompt guides contextual analysis with formatting rules

### Frontend Design
- **Agent Transparency**: Tool calls are visible to the user, showing the agent's reasoning
- **No Framework Overhead**: Vanilla JS for simplicity and fast loading
- **XSS Prevention**: HTML escaping before markdown conversion

## File Structure

```
inmarket-agentic-weather/
├── README.md                 # This file
├── .env                      # Environment variables (git-ignored)
├── requirements.txt          # Python dependencies (references subdirs)
├── start-all.bat             # Windows startup script
│
├── mcp-server/
│   ├── requirements.txt      # flask, requests, python-dotenv
│   ├── server.py             # MCP Server (JSON-RPC 2.0)
│   ├── tools.py              # WeatherAPIClient with 3 tools
│   └── config.py             # Environment configuration
│
├── backend/
│   ├── requirements.txt      # anthropic, flask, flask-cors, requests
│   ├── app.py                # Flask application + CORS
│   ├── agent.py              # WeatherAgent (Claude tool use + agentic loop)
│   ├── prompts.py            # System prompt + example queries
│   └── config.py             # Environment configuration
│
└── frontend/
    ├── index.html             # Chat UI
    ├── styles.css             # Styling (gradient theme, responsive)
    └── app.js                 # API calls, markdown rendering, tool call display
```

## Deployment Considerations

- **Docker**: Each service as a container with docker-compose orchestration
- **Kubernetes**: Separate deployments, ConfigMaps for env, Secrets for API keys
- **Serverless**: MCP Server + Backend as Lambda/Cloud Functions, Frontend on S3/CDN
- **Security**: Rate limiting, input validation, API key rotation via secrets management

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP Server won't start | Check port 8001 is free; verify OPENWEATHER_API_KEY in .env |
| Backend returns errors | Ensure MCP Server is running; check ANTHROPIC_API_KEY is valid |
| Frontend can't connect | Verify backend is on port 8000; check browser console for CORS |
| Agent returns empty | Check backend terminal logs for Claude API errors |

## License

MIT

## Contact

InMarket AI Builder Interview Project
