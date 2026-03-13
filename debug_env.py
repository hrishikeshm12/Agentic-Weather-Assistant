import os
from dotenv import load_dotenv

load_dotenv()

print("=== ENV Variables ===")
print(f"ANTHROPIC_API_KEY: {repr(os.getenv('ANTHROPIC_API_KEY'))}")
print(f"OPENWEATHER_API_KEY: {repr(os.getenv('OPENWEATHER_API_KEY'))}")

print("\n=== Raw .env content ===")
with open('.env', 'r') as f:
    content = f.read()
    print(content)
