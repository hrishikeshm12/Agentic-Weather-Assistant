"""
Configuration management for MCP Server
"""

import os
from dotenv import dotenv_values

# Load environment variables
_env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
_config = dotenv_values(_env_file) if os.path.exists(_env_file) else {}

def get_env(key: str, default: str = None) -> str:
    """Get environment variable with fallback to .env file"""
    # First try OS environment
    value = os.getenv(key)
    if value:
        return value

    # Then try .env file
    value = _config.get(key)
    if value:
        return value

    # Finally return default
    return default


# API Keys
OPENWEATHER_API_KEY = get_env('OPENWEATHER_API_KEY')

# Server Configuration
FLASK_ENV = get_env('FLASK_ENV', 'development')
MCP_SERVER_PORT = int(get_env('MCP_SERVER_PORT', '8001'))
DEBUG = get_env('DEBUG', 'False').lower() in ('true', '1', 'yes')
