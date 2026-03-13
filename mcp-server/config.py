"""
Configuration for MCP Server
"""

import os
import sys
from dotenv import load_dotenv

# Load .env from project root
project_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(project_root, '.env')

# Load environment variables
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
else:
    load_dotenv(override=True)

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '').strip('"\'')
MCP_SERVER_PORT = int(os.getenv('MCP_SERVER_PORT', 8001))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

if not OPENWEATHER_API_KEY:
    print("⚠️  WARNING: OPENWEATHER_API_KEY not set in .env")
