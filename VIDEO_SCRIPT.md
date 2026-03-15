# Video Script — Rehearsal-Ready
# Total Duration: ~10 minutes
# Recording Tool: Loom (free) — shows face bubble + screen share

---

## SETUP BEFORE RECORDING

1. **Loom**: Install from loom.com (free plan = 25 videos, 5 min each — use paid or use OBS + webcam overlay for longer)
   - Alternative: OBS Studio (free, unlimited) with webcam overlay
   - Alternative: ScreenRec (mentioned in PDF)
2. **Browser**: Open http://localhost:8002 (Weather Agent UI)
3. **Terminal**: Have the 3 service terminals visible (minimized, ready to show)
4. **IDE**: Open the project in VS Code / Cursor with these files tabbed:
   - `agent.py` (most important)
   - `server.py`
   - `prompts.py`
   - `PROMPTS_USED.md`
5. **Face**: Good lighting, clean background, look at camera
6. **Browser zoom**: 110-125%
7. **IDE font size**: 16-18px

---

## PART 1: INTRODUCTION (45 seconds)

**[Camera: Your face, visible on screen. Screen: Weather Agent UI in browser]**

> "Hi, I'm [Your Name], and this is my submission for the AI Builder role at InMarket."

> "I've built an end-to-end agentic weather assistant. It integrates the OpenWeather API through an MCP Server, uses Claude AI with native tool calling for intelligent reasoning, and presents everything through a chat-based frontend."

> "In this video, I'll walk through the architecture, show you the prompts I used in my agentic IDE to build each component, give a live demo, and discuss deployment and documentation strategy."

**[Pause 1 second]**

---

## PART 2: SELECTED API & CORE FUNCTION (1 minute)

**[Screen: Open browser tab to openweathermap.org/api]**

> "I chose the OpenWeather API because it offers three distinct endpoints on the free tier, which makes it perfect for demonstrating multi-tool agentic behavior."

> "The three core functions I'm wrapping are:
> - **Current Weather** — real-time temperature, humidity, wind, and conditions for any city
> - **5-Day Forecast** — hourly predictions grouped by day
> - **City Search** — geocoding to find cities by name"

> "Having three separate tools is important because it lets the LLM agent make autonomous decisions about WHICH tool to call and WHEN — which is the core of agentic behavior."

---

## PART 3: MCP SERVER ARCHITECTURE (2 minutes)

**[Screen: Switch to IDE → open server.py]**

> "The first layer is the MCP Server, running on port 8001. MCP stands for Model Context Protocol — it's a standardized way to expose API capabilities as tools that an LLM can call."

**[Scroll to show the /call endpoint]**

> "The key endpoint is /call, which implements JSON-RPC 2.0. When the backend agent wants weather data, it sends a JSON-RPC request with the method name and parameters. The MCP Server validates the request, dispatches to the correct tool, and returns a structured response."

**[Switch to tools.py, show the WeatherAPIClient class]**

> "The actual API calls live in tools.py — a clean WeatherAPIClient that wraps OpenWeather's REST API. Notice how the MCP Server knows NOTHING about AI or LLMs. It's purely a data access layer. This separation of concerns means I could swap the AI backend without touching the MCP Server, or add new data sources without changing the agent."

**[Switch to config.py briefly]**

> "API keys are loaded from environment variables via a .env file, never hardcoded, never exposed to the frontend. The .env file is gitignored."

**Key phrase to say:**
> "The benefit of the MCP architecture is clean separation — the MCP Server is a standalone microservice that could be reused by any client, not just this AI agent."

---

## PART 4: AGENTIC IDE PROMPTS (2 minutes)

**[Screen: Open PROMPTS_USED.md in the IDE]**

> "Let me show you the prompts I used in my agentic IDE to build this project. I used Claude Code as my agentic IDE — it runs directly in the terminal and can read, write, and execute code autonomously."

**[Scroll through the prompts document slowly]**

> "For the MCP Server, I prompted: 'Create a WeatherAPIClient class with three tools — get_current_weather, get_forecast, and search_cities. Use metric units, include error handling and type hints.' The IDE generated the complete tools.py with proper API wrapping in one pass."

**[Scroll to Prompt 3.1]**

> "For the agent backend, this was the most important prompt. I asked for a WeatherAgent class using Anthropic SDK directly — not LangChain. I'll explain why in a moment. The prompt specified the agentic loop pattern: send the query to Claude, if Claude responds with tool_use, call the MCP Server, feed results back, and loop until Claude has enough information to give a final answer."

**[Scroll to Prompt 5.2]**

> "Here's an example of iterative debugging with the IDE. The agent's logs weren't showing up in the terminal. I described the symptom, and the IDE identified that Python's logging.basicConfig was being called AFTER the agent module was imported, so the logger was already configured. It moved the config before the import and added force=True. This kind of diagnostic prompting is where agentic IDEs really shine — you describe the problem, not the solution."

**Key phrase to say:**
> "The agentic IDE accelerated development significantly. What would normally be hours of docs-reading and trial-and-error became iterative prompt-and-refine cycles."

---

## PART 5: LLM AGENT SETUP — WHY NOT LANGCHAIN (1.5 minutes)

**[Screen: Open agent.py, scroll to show the TOOLS definition and the agentic loop]**

> "Now, the PDF mentions LangChain, but I made a deliberate architectural decision to use Claude's native tool_use API instead. Let me explain why."

> "LangChain's AgentExecutor is essentially a wrapper that does three things: sends your query to the LLM with tool definitions, processes tool_use responses, and loops until done. That's exactly what my agentic loop does here..."

**[Highlight the for loop in process_query]**

> "...but with full control. I define the tools with Claude's native input_schema format, I manage the message history myself, and I track every tool call for frontend transparency."

> "The advantages over LangChain are:
> - **Fewer dependencies** — no pydantic version conflicts, no framework overhead
> - **Full transparency** — I can log and return every tool call to the frontend
> - **Direct control** — I manage conversation history, iteration limits, and error handling exactly how I want
> - **The agentic pattern is identical** — Claude autonomously decides which tools to call, just like LangChain's agent would"

> "The PDF says 'LangChain or similar framework.' Claude's native tool_use IS the underlying mechanism that LangChain wraps. Using it directly is like using React hooks instead of a state management library — it's the same pattern, with less abstraction."

---

## PART 6: PROMPT ENGINEERING (1 minute)

**[Screen: Open prompts.py]**

> "Effective prompt engineering is what makes the difference between a data dump and an intelligent assistant."

**[Show the SYSTEM_PROMPT]**

> "My system prompt does four things:
> 1. Defines the agent's role and personality
> 2. Lists the available tools so Claude knows what it can call
> 3. Sets formatting rules — bold for key values, bullet points for lists, paragraph breaks
> 4. Instructs contextual analysis — don't just say '15 degrees,' say 'it's 15°C which feels colder due to wind chill'"

> "This prompt engineering ensures the responses are user-friendly and contextually relevant, not just raw API data."

---

## PART 7: LIVE DEMO (2-3 minutes)

**[Screen: Browser at http://localhost:8002]**

### Demo 1: Basic Query
> "Let me show the end-to-end experience. I'll ask: 'What's the weather in London?'"

**[Type and send. Wait for response.]**

> "Notice three things happening:
> 1. The 'Agent Actions' panel appears — showing that Claude called get_current_weather with city: London
> 2. It shows a result preview — the temperature and conditions
> 3. The response below is contextual — it doesn't just list numbers, it provides analysis"

### Demo 2: Multi-Tool Agentic Behavior
> "Now watch this — I'll ask: 'Compare the weather in Tokyo and New York'"

**[Type and send. Wait for response.]**

> "Look at the Agent Actions panel — Claude called the tool TWICE, once for each city, then synthesized a comparison. This is true agentic behavior — the LLM autonomously decided it needed two tool calls to answer my question. I didn't hardcode that logic."

### Demo 3: Conversation Memory
> "Here's where multi-turn context matters. I'll ask: 'Which one should I visit this weekend?'"

**[Type and send.]**

> "The agent remembers we were talking about Tokyo and New York. It uses that context plus the forecast tool to give a travel recommendation. This is conversation history in action."

### Demo 4: Reset
> "I can click 'New Chat' to clear the conversation context and start fresh."

**[Click New Chat button]**

---

## PART 8: DEPLOYMENT DISCUSSION (1 minute)

**[Screen: Can stay on the app or show the README deployment section]**

> "For production deployment, I'd take a containerized approach."

> "**Docker**: Each service gets its own Dockerfile. Docker Compose orchestrates all three with proper networking — the frontend talks to the backend, the backend talks to the MCP Server, and only the frontend is exposed publicly."

> "**Kubernetes**: For scale, each service becomes a Deployment with its own Horizontal Pod Autoscaler. The MCP Server might need more replicas since it handles external API calls. API keys go into Kubernetes Secrets, configuration into ConfigMaps."

> "**Serverless alternative**: The MCP Server and Backend could run as AWS Lambda functions behind API Gateway. The frontend goes on S3 with CloudFront CDN. This gives you pay-per-request pricing and zero ops overhead."

> "**Security in production**: API keys in AWS Secrets Manager or HashiCorp Vault with automatic rotation. Rate limiting on all endpoints. CORS locked down to specific origins. Input validation and sanitization on every request."

---

## PART 9: DOCUMENTATION PHILOSOPHY (1 minute)

**[Screen: Show README.md in IDE, scroll through it]**

> "For documentation, I think about two audiences."

> "**For a collaborating developer**: The README has an architecture diagram, API reference tables, and debugging commands. They can understand the system in 5 minutes and start contributing."

> "**For a new developer taking over**: The step-by-step setup guide walks through everything — environment variables, virtual environment, installing dependencies, and running all three services. The troubleshooting table covers the most common issues."

> "I also documented the file structure and key design decisions — like why I chose Anthropic SDK over LangChain. In a team context, I'd add Architecture Decision Records, or ADRs, to capture these rationale documents formally."

> "The code itself is documented with docstrings and clear function names. I believe code should be self-documenting where possible, with comments reserved for the 'why,' not the 'what.'"

---

## PART 10: CLOSING (30 seconds)

**[Camera: Your face prominently visible]**

> "To summarize — this project demonstrates:
> - A clean microservice architecture with MCP protocol
> - Agentic AI with Claude's native tool calling and multi-step reasoning
> - Multi-turn conversation memory
> - Frontend transparency showing the agent's decision process
> - And it was built entirely using an agentic IDE with iterative prompting."

> "The full code is on GitHub with a comprehensive README. Thank you for your time, and I look forward to discussing this further."

**[Smile, hold for 2 seconds, then stop recording]**

---

## TIMING BREAKDOWN

| Section | Duration | Running Total |
|---------|----------|---------------|
| Introduction | 0:45 | 0:45 |
| API Selection | 1:00 | 1:45 |
| MCP Architecture | 2:00 | 3:45 |
| IDE Prompts | 2:00 | 5:45 |
| LLM Agent / LangChain | 1:30 | 7:15 |
| Prompt Engineering | 1:00 | 8:15 |
| Live Demo | 2:30 | 10:45 |
| Deployment | 1:00 | 11:45 |
| Documentation | 1:00 | 12:45 |
| Closing | 0:30 | 13:15 |

**Note:** If you need to cut time, combine sections 5+6 (LLM + Prompt Engineering) and shorten Demo to 2 queries.

---

## REHEARSAL CHECKLIST

- [ ] Practice 2-3 times before recording
- [ ] Make sure all 3 services are running before you hit record
- [ ] Test each demo query works before recording
- [ ] Check webcam and microphone quality
- [ ] Close notifications, Slack, email — no popup interruptions
- [ ] Have a glass of water nearby
- [ ] Speak slowly and clearly — it's better to be slightly slow than to rush
- [ ] Make eye contact with the camera periodically, not just the screen
- [ ] If you make a mistake, just pause and continue — don't restart the entire recording
