"""
Configuration for Backend Agent
"""

import os
from dotenv import load_dotenv

# Load .env from project root
project_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(project_root, '.env')

# Load environment variables
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
else:
    load_dotenv(override=True)

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '').strip('"\'')
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8001')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8000))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

# Allow missing API key at import time (will error when used)
# if not ANTHROPIC_API_KEY:
#     raise ValueError("ANTHROPIC_API_KEY environment variable not set")
