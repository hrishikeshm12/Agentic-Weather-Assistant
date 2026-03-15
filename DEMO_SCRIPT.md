# Demo Video Script - Agentic Weather Assistant

## Video Structure (Target: 8-10 minutes)

---

## SECTION 1: Introduction (30 seconds)

**[Screen: Browser showing the Weather Agent UI]**

> "Hi, I'm [Your Name]. This is my submission for the InMarket AI Builder role.
> I built an end-to-end agentic weather assistant that combines a public API,
> an MCP Server, Claude AI with native tool calling, and a chat-based frontend.
> Let me walk you through the architecture, the development process, and a live demo."

---

## SECTION 2: Architecture Overview (2 minutes)

**[Screen: Show the README architecture diagram or draw on a whiteboard tool]**

> "The application has three microservices running locally:"

> "First, the **MCP Server** on port 8001. This wraps the OpenWeather API into
> three standardized tools using JSON-RPC 2.0. It handles API key management
> and data formatting. The key design principle here is separation of concerns -
> the MCP Server knows nothing about AI or business logic. It just exposes clean
> tool interfaces."

> "Second, the **Backend Agent** on port 8000. This is where the AI reasoning
> happens. It uses Claude's native tool_use feature - not a framework wrapper.
> When a user asks a question, Claude autonomously decides which MCP tools to call,
> processes the results, and can make multiple tool calls if needed - for example,
> to compare weather in two cities. It also maintains conversation history for
> follow-up questions."

> "Third, the **Frontend** on port 8002. A vanilla HTML/CSS/JS chat interface.
> It shows the user which tools the agent called and their results, providing
> transparency into the AI's decision-making process."

**Key points to emphasize:**
- JSON-RPC 2.0 protocol between Backend and MCP Server
- Claude's native tool_use (not LangChain) - explain why: direct control, fewer dependencies
- Agentic loop pattern: Claude decides when it has enough data to respond
- Conversation history enables multi-turn interactions

---

## SECTION 3: Agentic Development Process (2 minutes)

**[Screen: Show your IDE (Cursor/VS Code with Copilot)]**

> "I used an agentic IDE throughout development. Let me show you some key moments."

**Show examples of:**
1. **Prompt-driven development**: "I scaffolded the MCP Server tools by describing what I needed - a weather API client with three tools for current weather, forecasts, and city search."

2. **Iterative refinement**: "When I hit compatibility issues with LangChain on Python 3.14, I used the IDE to pivot to Claude's native SDK. The agent helped me rewrite the entire agent.py in one iteration."

3. **Debugging with AI**: "The IDE helped me diagnose environment variable loading issues across different working directories, and fix logging configuration to ensure agent logs were visible."

> "The agentic IDE significantly accelerated development - what might have taken
> a day of debugging was resolved in minutes through iterative prompting."

---

## SECTION 4: Live Demo (3-4 minutes)

**[Screen: Browser at http://localhost:8002]**

### Demo Scenario 1: Basic Weather Query
> "Let me ask: 'What's the weather in London?'"

**[Type and send the query. Wait for response.]**

> "Notice a few things:
> - The 'Agent Actions' panel shows the tool call: 'get current weather (city: London)'
> - The result preview shows the temperature and conditions
> - The response includes contextual analysis - not just raw data"

### Demo Scenario 2: Multi-tool Query (Comparison)
> "Now let's try: 'Compare the weather in Tokyo and New York'"

**[Send the query]**

> "Here you can see the agentic loop in action - Claude called the tool TWICE,
> once for Tokyo and once for New York, then synthesized a comparison. This is
> the power of the agentic pattern - the LLM autonomously decides how many
> tool calls it needs."

### Demo Scenario 3: Follow-up Question (Conversation History)
> "Now I'll ask a follow-up: 'Which one should I visit this weekend?'"

**[Send the query]**

> "The agent remembers the previous context about Tokyo and New York, and uses
> that along with forecast data to give a travel recommendation. This demonstrates
> multi-turn conversation memory."

### Demo Scenario 4: Forecast
> "Let's try: 'What's the 5-day forecast for San Francisco?'"

**[Send the query]**

> "This calls the get_forecast tool, which returns daily highs, lows, and conditions."

### Demo Scenario 5: Reset
> "Finally, I'll click 'New Chat' to show the conversation reset feature."

---

## SECTION 5: Code Walkthrough (1-2 minutes)

**[Screen: IDE showing code]**

### agent.py - The Heart of the Application
> "The WeatherAgent class defines three tools with Claude's input_schema format.
> The process_query method implements the agentic loop: it sends the query to Claude,
> processes any tool_use responses by calling the MCP Server, feeds results back,
> and loops until Claude issues an end_turn."

**[Highlight the agentic loop, tool call processing, conversation history]**

### server.py - MCP Server
> "The MCP Server is a Flask app that accepts JSON-RPC 2.0 requests, validates them,
> and dispatches to the appropriate tool function. It's completely decoupled from
> the AI layer."

### prompts.py - Prompt Engineering
> "The system prompt instructs Claude on formatting, tool usage, and response style.
> Good prompt engineering is critical - it's what makes the responses contextual
> rather than just data dumps."

---

## SECTION 6: Deployment & Documentation Discussion (1 minute)

> "For production deployment, I'd containerize each service with Docker and use
> docker-compose for orchestration. For scale, Kubernetes with separate deployments
> and horizontal pod autoscaling."

> "For a serverless approach, the MCP Server and Backend could run as AWS Lambda
> or Google Cloud Functions, with the frontend on S3 behind CloudFront."

> "Key security considerations: API keys in secrets management (AWS Secrets Manager
> or Vault), rate limiting on all endpoints, input validation, and CORS lockdown
> to specific origins."

> "For documentation, I structured the README with architecture diagrams,
> setup instructions, API reference, and troubleshooting. For a team context,
> I'd add ADRs (Architecture Decision Records) for key choices like the decision
> to use Claude's native SDK over LangChain."

---

## SECTION 7: Wrap-up (30 seconds)

> "To summarize: this project demonstrates a clean microservice architecture with
> MCP protocol, agentic AI with Claude's native tool calling, multi-turn
> conversation support, and a transparent frontend showing the agent's reasoning.
> The codebase is clean, well-documented, and ready for extension."

> "Thank you for your time. The full code is on GitHub."

---

## Recording Tips

1. **Screen resolution**: Use 1920x1080 for clear recording
2. **Font size**: Increase IDE font to 16-18px for readability
3. **Browser zoom**: Set to 110-125% so the chat UI is clearly visible
4. **Terminal**: Keep the backend terminal visible (split screen) to show logs during demo
5. **Pace**: Speak slowly and clearly, pause after each tool call to explain what happened
6. **Energy**: Be enthusiastic about the architecture decisions - the evaluators want to see passion

## Demo Queries to Practice

1. "What's the weather in London?" - basic single tool call
2. "Compare the weather in Tokyo and New York" - multi-tool agentic behavior
3. "Which one should I visit this weekend?" - conversation history follow-up
4. "What's the 5-day forecast for San Francisco?" - forecast tool
5. "Search for cities named Portland" - city search tool
6. "Is it a good day for outdoor activities in Sydney?" - contextual reasoning
