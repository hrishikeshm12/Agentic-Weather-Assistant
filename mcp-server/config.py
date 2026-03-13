"""
MCP Server Configuration
Loads environment variables and provides configuration values
"""

import os
from dotenv import load_dotenv

# Load .env from project root
project_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path if os.path.exists(env_path) else None, override=True)

# OpenWeather API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Server Configuration
MCP_SERVER_PORT = int(os.getenv('MCP_SERVER_PORT', 8001))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

# Validate required configuration
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable is required")
