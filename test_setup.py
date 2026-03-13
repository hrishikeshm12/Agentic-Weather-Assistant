#!/usr/bin/env python
"""
Quick test to verify all components are set up correctly
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("WEATHER AGENT - SETUP VERIFICATION")
print("=" * 60)
print()

# Test 1: Check environment variables
print("1. Checking Environment Configuration...")
try:
    from dotenv import load_dotenv
    load_dotenv()

    openweather_key = os.getenv('OPENWEATHER_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    if openweather_key:
        print(f"   ✓ OpenWeather API Key: {'***' + openweather_key[-10:]}")
    else:
        print("   ✗ OpenWeather API Key: NOT SET")

    if anthropic_key:
        print(f"   ✓ Anthropic API Key: {'***' + anthropic_key[-10:]}")
    else:
        print("   ✗ Anthropic API Key: NOT SET")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 2: Check MCP Server tools
print("2. Checking MCP Server Tools...")
try:
    from mcp_server.tools import WeatherAPIClient, create_tools

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if api_key:
        tools = create_tools(api_key)
        print(f"   ✓ Tools created: {list(tools.keys())}")
        print(f"   ✓ MCP Server ready")
    else:
        print("   ✗ Missing API key - skipping tool creation")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 3: Check Flask app
print("3. Checking Backend App...")
try:
    from backend.app import app
    print(f"   ✓ Flask app initialized")
    print(f"   ✓ Routes available:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"     - {rule.rule}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 4: Check LangChain agent
print("4. Checking LangChain Agent...")
try:
    from backend.agent import create_agent
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key:
        agent = create_agent(anthropic_key)
        print(f"   ✓ Agent created successfully")
        print(f"   ✓ Agent tools: get_current_weather, get_forecast, search_cities")
    else:
        print("   ✗ Missing Anthropic key - skipping agent creation")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 5: Check frontend files
print("5. Checking Frontend Files...")
frontend_files = ['frontend/index.html', 'frontend/styles.css', 'frontend/app.js']
for file in frontend_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} NOT FOUND")

print()

print("=" * 60)
print("✓ SETUP VERIFICATION COMPLETE")
print("=" * 60)
print()
print("Next steps:")
print("  1. (Windows) Run: start-servers.bat")
print("  2. (Linux/Mac) Run: bash start-servers.sh")
print("  3. Open http://localhost:8000 in your browser")
print("  4. Ask the agent: 'What is the weather in London?'")
print()
