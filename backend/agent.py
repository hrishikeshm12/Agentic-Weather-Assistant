"""
LangChain Agent for Weather Intelligence
Handles tool calling and conversation management
"""

import os
import json
import logging
import requests
from typing import Any, Dict, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool, ToolException
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts import get_system_prompt
from config import MCP_SERVER_URL, ANTHROPIC_API_KEY

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
            raise ToolException(f"MCP error: {data['error']['message']}")

        return data.get('result', {})

    except requests.exceptions.RequestException as e:
        raise ToolException(f"MCP Server error: {str(e)}")
    except Exception as e:
        raise ToolException(f"Unexpected error: {str(e)}")


# Define tools for LangChain
@tool
def get_current_weather(city: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current weather conditions for a city.

    Args:
        city: Name of the city
        country: Optional ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')

    Returns:
        Current weather data including temperature, conditions, humidity, wind speed
    """
    logger.info(f"Getting current weather for {city}, {country}")
    result = call_mcp_tool('get_current_weather', city=city, **(
        {'country': country} if country else {}
    ))
    return result


@tool
def get_forecast(city: str, country: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast for a city.

    Args:
        city: Name of the city
        country: Optional ISO 3166-1 alpha-2 country code
        days: Number of days to forecast (default 5)

    Returns:
        Weather forecast data with daily predictions
    """
    logger.info(f"Getting {days}-day forecast for {city}, {country}")
    result = call_mcp_tool('get_forecast', city=city, **(
        {'country': country} if country else {}
    ), days=days)
    return result


@tool
def search_cities(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search for cities by name to get their coordinates and details.

    Useful when you need to disambiguate city names or find exact coordinates.

    Args:
        query: City name to search for
        limit: Maximum number of results (default 5)

    Returns:
        List of matching cities with coordinates and country information
    """
    logger.info(f"Searching for cities matching '{query}'")
    result = call_mcp_tool('search_cities', query=query, limit=limit)
    return result


def create_agent(api_key: Optional[str] = None) -> AgentExecutor:
    """
    Create and configure the weather agent with LangChain

    Args:
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)

    Returns:
        Configured AgentExecutor
    """
    if not api_key:
        api_key = ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Initialize LLM
    llm = ChatAnthropic(
        model='claude-3-5-sonnet-20241022',
        api_key=api_key,
        temperature=0.7,
        max_tokens=2048
    )

    # Define tools
    tools = [get_current_weather, get_forecast, search_cities]

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ('system', get_system_prompt()),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        ('human', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ])

    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create executor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=10,
        handle_parsing_errors=True
    )

    return executor


def process_query(executor: AgentExecutor, user_query: str) -> str:
    """
    Process a user query through the agent

    Args:
        executor: The AgentExecutor instance
        user_query: User's question or request

    Returns:
        Agent's response
    """
    try:
        logger.info(f"Processing query: {user_query}")
        result = executor.invoke({'input': user_query})
        response = result.get('output', 'I could not process your request.')
        logger.info(f"Query processed successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"I encountered an error: {str(e)}. Please try again."
