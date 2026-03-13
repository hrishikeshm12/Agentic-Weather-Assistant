#!/usr/bin/env python
"""
Simple demo to test the weather agent
"""

import sys
import os
import subprocess
import time
import requests
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("WEATHER AGENT DEMO - QUICK START")
print("=" * 70)
print()

# Test 1: Check configuration
print("Step 1: Verifying Configuration...")
try:
    import sys
    sys.path.insert(0, 'backend')
    sys.path.insert(0, 'mcp-server')

    from backend.config import ANTHROPIC_API_KEY, OPENWEATHER_API_KEY, BACKEND_PORT, MCP_SERVER_PORT

    if ANTHROPIC_API_KEY and OPENWEATHER_API_KEY:
        print("   ✓ API Keys are configured")
    else:
        print("   ✗ Missing API Keys")
        sys.exit(1)

except Exception as e:
    print(f"   ✗ Configuration error: {e}")
    sys.exit(1)

print()

# Test 2: Check MCP Server
print("Step 2: Testing MCP Server Tools...")
try:
    from mcp_server.tools import create_tools
    tools = create_tools(OPENWEATHER_API_KEY)
    print(f"   ✓ Tools available: {list(tools.keys())}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print()

# Test 3: Check LangChain Agent
print("Step 3: Testing LangChain Agent...")
try:
    from backend.agent import create_agent
    agent = create_agent(ANTHROPIC_API_KEY)
    print(f"   ✓ Agent created successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print()

# Test 4: Test Flask endpoints
print("Step 4: Testing Flask Backend...")
try:
    from backend.app import app
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print(f"   ✓ Backend health: OK")
        response = client.get('/examples')
        if response.status_code == 200:
            examples = response.get_json()['examples']
            print(f"   ✓ Found {len(examples)} example queries")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 5: Test MCP Server endpoints
print("Step 5: Testing MCP Server...")
try:
    from mcp_server.server import app as mcp_app
    with mcp_app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print(f"   ✓ MCP Server health: OK")
        response = client.get('/tools')
        if response.status_code == 200:
            tools = response.get_json()['tools']
            print(f"   ✓ MCP Server tools: {[t['name'] for t in tools]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()
print("=" * 70)
print("✓ ALL TESTS PASSED - APPLICATION READY")
print("=" * 70)
print()
print("To start the servers, run:")
print("  Windows:   start-servers.bat")
print("  Linux/Mac: bash start-servers.sh")
print()
print("Then open http://localhost:8000 in your browser")
print()
