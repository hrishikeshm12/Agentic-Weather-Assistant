"""
Weather Agent using Claude's Native Tool Use
Direct integration with MCP Server tools
"""

import os
import sys
import json
import logging
import requests
from typing import Any, Dict, Optional
from anthropic import Anthropic

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import MCP_SERVER_URL, ANTHROPIC_API_KEY
from prompts import get_system_prompt

logger = logging.getLogger(__name__)


def call_mcp_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Call a tool on the MCP server using JSON-RPC 2.0

    Args:
        tool_name: Name of the tool to call
        **kwargs: Tool parameters

    Returns:
        Tool result
    """
    payload = {
        'jsonrpc': '2.0',
        'method': tool_name,
        'params': kwargs,
        'id': '1'
    }

    try:
        response = requests.post(
            f'{MCP_SERVER_URL}/call',
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            raise Exception(f"MCP error: {data['error']['message']}")

        return data.get('result', {})

    except requests.exceptions.RequestException as e:
        raise Exception(f"MCP Server error: {str(e)}")
    except Exception as e:
        raise Exception(f"Tool call failed: {str(e)}")


class WeatherAgent:
    """Weather agent using Claude's native tool use with conversation memory"""

    TOOLS = [
        {
            "name": "get_current_weather",
            "description": "Get current weather conditions for a city",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    },
                    "country": {
                        "type": "string",
                        "description": "Optional ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "get_forecast",
            "description": "Get 5-day weather forecast for a city",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    },
                    "country": {
                        "type": "string",
                        "description": "Optional ISO 3166-1 alpha-2 country code"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (default 5)",
                        "default": 5
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "search_cities",
            "description": "Search for cities by name",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "City name to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    ]

    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            api_key = ANTHROPIC_API_KEY
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-opus-4-1"
        # Conversation history for multi-turn context
        self.conversation_history = []
        # Keep last N exchanges to avoid token limits
        self.max_history = 10

    def _trim_history(self):
        """Keep conversation history within limits"""
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process a user query with tool calling. Returns response with tool call metadata."""
        logger.info(f"Processing query: {user_query}")

        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })
        self._trim_history()

        # Build messages from conversation history
        messages = list(self.conversation_history)

        # Track tool calls for visibility
        tool_calls_log = []

        try:
            # Agentic loop
            max_iterations = 10
            for iteration in range(max_iterations):
                logger.info(f"Agent iteration {iteration + 1}")

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    system=get_system_prompt(),
                    tools=self.TOOLS,
                    messages=messages
                )

                logger.info(f"Stop reason: {response.stop_reason}")

                # Add assistant response to messages
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Check if we're done
                if response.stop_reason == "end_turn":
                    # Extract final text response
                    final_text = "I have completed my analysis."
                    for block in response.content:
                        if hasattr(block, 'text'):
                            final_text = block.text
                            break

                    # Save assistant response to conversation history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_text
                    })

                    return {
                        "text": final_text,
                        "tool_calls": tool_calls_log
                    }

                # Process tool uses
                if response.stop_reason == "tool_use":
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input

                            logger.info(f"Calling tool: {tool_name} with input: {tool_input}")

                            # Log tool call for frontend visibility
                            tool_call_entry = {
                                "tool": tool_name,
                                "input": tool_input,
                                "status": "success"
                            }

                            try:
                                result = call_mcp_tool(tool_name, **tool_input)
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": json.dumps(result)
                                })
                                tool_call_entry["result_preview"] = _summarize_result(tool_name, result)
                            except Exception as e:
                                logger.error(f"Tool error: {str(e)}")
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": f"Error: {str(e)}"
                                })
                                tool_call_entry["status"] = "error"
                                tool_call_entry["result_preview"] = str(e)

                            tool_calls_log.append(tool_call_entry)

                    # Add tool results
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })
                else:
                    # Unexpected stop reason
                    break

            return {
                "text": "I encountered an issue processing your request.",
                "tool_calls": tool_calls_log
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "text": f"I encountered an error: {str(e)}. Please try again.",
                "tool_calls": tool_calls_log
            }


def _summarize_result(tool_name: str, result: Dict) -> str:
    """Create a brief summary of tool result for frontend display"""
    if tool_name == "get_current_weather":
        city = result.get("city", "Unknown")
        temp = result.get("temperature", "?")
        condition = result.get("description", "")
        return f"{city}: {temp}°C, {condition}"
    elif tool_name == "get_forecast":
        city = result.get("city", "Unknown")
        days = len(result.get("forecasts", []))
        return f"{city}: {days}-day forecast loaded"
    elif tool_name == "search_cities":
        count = len(result.get("results", []))
        return f"Found {count} cities"
    return "Data retrieved"


def create_agent(api_key: Optional[str] = None) -> WeatherAgent:
    """Create a weather agent"""
    return WeatherAgent(api_key)


def process_query(agent: WeatherAgent, user_query: str) -> Dict[str, Any]:
    """Process a query through the agent. Returns dict with 'text' and 'tool_calls'."""
    return agent.process_query(user_query)
