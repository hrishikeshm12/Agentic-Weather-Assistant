# Prompts Used During Development

## Overview
This document captures the key prompts used within the agentic IDE (Claude Code / Cursor) during the development of the Weather Agent application. These prompts demonstrate the agentic development workflow — iterative, prompt-driven building of each component.

---

## Phase 1: Project Scaffolding

### Prompt 1.1 — Initial Project Setup
```
I need to build an agentic web app for an interview project. The requirements are:
1. Public REST API integration (I want to use OpenWeather API - free tier)
2. MCP Server wrapper for the API using JSON-RPC 2.0
3. LLM Agent backend using Claude API with tool calling
4. Frontend web app (simple chat interface)

Create the project structure with separate folders for frontend, backend, and mcp-server.
Include requirements.txt for each Python service and a root requirements.txt that references them.
Set up .env handling for API keys (OpenWeather + Anthropic) with python-dotenv.
```

**Result:** Generated the full folder structure, config.py files for both services, and requirements.txt files.

---

## Phase 2: MCP Server Development

### Prompt 2.1 — Weather API Client
```
Create a WeatherAPIClient class in mcp-server/tools.py that wraps the OpenWeather API
with three tools:
1. get_current_weather(city, country?) - returns temperature, humidity, wind, conditions
2. get_forecast(city, country?, days?) - returns 5-day forecast grouped by day
3. search_cities(query, limit?) - searches cities using the Geocoding API

Use metric units (Celsius). Include proper error handling and type hints.
Also create the tool definitions dict that maps tool names to their function + JSON schema.
```

**Result:** Generated `tools.py` with the WeatherAPIClient class and `create_tools()` function.

### Prompt 2.2 — JSON-RPC 2.0 Server
```
Create the MCP Server in mcp-server/server.py as a Flask app implementing JSON-RPC 2.0.

Endpoints needed:
- GET /health - health check
- GET /tools - list available tools with their schemas
- POST /call - JSON-RPC 2.0 tool invocation

The /call endpoint should validate JSON-RPC format (jsonrpc: "2.0", method, params, id),
dispatch to the correct tool, and return proper JSON-RPC responses including error codes
(-32700, -32601, -32602, -32603) for different failure types.
```

**Result:** Generated `server.py` with full JSON-RPC 2.0 compliance and error handling.

---

## Phase 3: LLM Agent Backend

### Prompt 3.1 — Claude Agent with Native Tool Use
```
Create a WeatherAgent class in backend/agent.py that uses the Anthropic SDK directly
(not LangChain) for tool calling.

Requirements:
- Define 3 tools (get_current_weather, get_forecast, search_cities) using Claude's
  input_schema format
- Implement an agentic loop: send query to Claude → if tool_use, call MCP Server via
  JSON-RPC → feed results back → loop until end_turn
- Max 10 iterations to prevent infinite loops
- Call MCP Server tools via HTTP POST to localhost:8001/call with JSON-RPC 2.0 format
- Include conversation history for multi-turn support
- Return tool call metadata alongside the response for frontend transparency

I chose Anthropic SDK over LangChain because:
1. Direct control over the agentic loop
2. Fewer dependencies and compatibility issues
3. Claude's native tool_use is more reliable than framework wrappers
```

**Result:** Generated the WeatherAgent class with full agentic loop, conversation history, and tool call tracking.

### Prompt 3.2 — System Prompt Engineering
```
Create a system prompt for the weather agent in backend/prompts.py. The prompt should:
- Define the agent's role as an intelligent weather assistant
- List the available tools and when to use each
- Include formatting rules (bold for key values, bullet points, paragraphs)
- Instruct the agent to provide contextual analysis, not just raw data
- Tell it to mention safety considerations for extreme weather
- Include temperature in both Celsius and Fahrenheit

Also add 5 example queries that the frontend can display.
```

**Result:** Generated `prompts.py` with a detailed system prompt and example queries.

### Prompt 3.3 — Flask Backend Server
```
Create backend/app.py as a Flask server with CORS support.

Endpoints:
- GET /health - returns agent status
- POST /query - accepts {query: string}, returns {response, tool_calls, success}
- GET /examples - returns example queries from prompts.py
- POST /reset - clears conversation history

Initialize the agent on startup. Configure logging BEFORE importing the agent module
so we can see agentic loop logs in the terminal.
```

**Result:** Generated `app.py` with all endpoints and proper logging configuration.

---

## Phase 4: Frontend Development

### Prompt 4.1 — Chat Interface
```
Create a chat-based frontend with vanilla HTML/CSS/JS (no framework).

Requirements:
- Clean chat UI with user messages on right, agent responses on left
- Example query buttons that populate the input field
- Loading indicator while agent is processing
- Markdown rendering for agent responses (bold, italic, code, bullet points)
- XSS prevention: escape HTML before converting markdown
- Health check on load to verify backend is running
- Gradient purple/blue theme, responsive design
```

**Result:** Generated `index.html`, `styles.css`, and `app.js` with the complete chat interface.

### Prompt 4.2 — Tool Call Transparency
```
Enhance the frontend to show which MCP tools the agent called for each response.
Display tool calls in a styled panel between the user message and agent response, showing:
- Tool name (human-readable)
- Input parameters
- Success/error status
- Brief result preview

This demonstrates the agentic pattern to the user - they can see the agent's
decision-making process.
```

**Result:** Added `addToolCallsMessage()` function and CSS for the Agent Actions panel.

---

## Phase 5: Integration & Debugging

### Prompt 5.1 — Environment Variable Fix
```
The .env file isn't being loaded correctly when running from different directories.
backend/config.py needs to find the .env file in the project root regardless of
which directory the script is run from. Use os.path.dirname(os.path.dirname(__file__))
to get the project root.
```

### Prompt 5.2 — Logging Fix
```
Agent iteration logs aren't showing in the terminal. The issue is that logging.basicConfig
in app.py runs AFTER the agent module is imported, so the agent's logger is already
configured. Move basicConfig BEFORE the agent import and use force=True to override.
```

### Prompt 5.3 — Startup Script
```
Create a Windows .bat file that starts all 3 services in separate terminal windows
with titles. Use 'cmd /k' to keep windows open so logs are visible.
```

**Result:** Generated `start-all.bat` for one-click startup.

---

## Phase 6: Enhancements

### Prompt 6.1 — Conversation History
```
Add multi-turn conversation support to the WeatherAgent. Maintain a conversation_history
list, trim it to prevent token overflow, and add a clear_history() method.
This allows follow-up questions like "Should I bring an umbrella?" after asking
about London's weather.
```

### Prompt 6.2 — README Polish
```
Update the README with:
- ASCII architecture diagram showing all 4 layers (Frontend → Backend → MCP → OpenWeather)
- How the agentic loop works section
- API reference tables
- Deployment considerations (Docker, K8s, Serverless)
- Troubleshooting table
- Accurate file structure
```
