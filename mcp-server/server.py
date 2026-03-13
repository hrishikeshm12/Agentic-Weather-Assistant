"""
MCP Server for OpenWeather API
Implements JSON-RPC 2.0 protocol for tool calling
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from tools import create_tools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize tools
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    logger.error("OPENWEATHER_API_KEY environment variable not set")
    raise ValueError("OPENWEATHER_API_KEY environment variable not set")

TOOLS = create_tools(API_KEY)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'MCP Server'}), 200


@app.route('/tools', methods=['GET'])
def list_tools():
    """List all available tools with their schemas"""
    tools_info = []
    for name, tool in TOOLS.items():
        tools_info.append({
            'name': name,
            'description': tool['description'],
            'parameters': tool['parameters']
        })
    return jsonify({'tools': tools_info}), 200


@app.route('/call', methods=['POST'])
def call_tool():
    """
    JSON-RPC 2.0 endpoint for calling tools

    Expected request format:
    {
        "jsonrpc": "2.0",
        "method": "tool_name",
        "params": {
            "param1": "value1",
            "param2": "value2"
        },
        "id": "request_id"
    }
    """
    try:
        data = request.get_json()

        # Validate JSON-RPC format
        if not data or 'jsonrpc' not in data or data['jsonrpc'] != '2.0':
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'message': 'Invalid Request',
                    'data': 'Missing or invalid jsonrpc field'
                },
                'id': data.get('id') if data else None
            }), 400

        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')

        # Check if tool exists
        if method not in TOOLS:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32601,
                    'message': 'Method not found',
                    'data': f'Tool "{method}" not available'
                },
                'id': request_id
            }), 400

        # Call the tool
        logger.info(f"Calling tool: {method} with params: {params}")
        tool = TOOLS[method]
        result = tool['function'](**params)

        logger.info(f"Tool {method} executed successfully")
        return jsonify({
            'jsonrpc': '2.0',
            'result': result,
            'id': request_id
        }), 200

    except TypeError as e:
        # Invalid parameters
        logger.error(f"Invalid parameters: {str(e)}")
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid params',
                'data': str(e)
            },
            'id': data.get('id') if 'data' in locals() else None
        }), 400

    except Exception as e:
        # General error
        logger.error(f"Tool execution failed: {str(e)}")
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': 'Internal error',
                'data': str(e)
            },
            'id': data.get('id') if 'data' in locals() else None
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service information"""
    return jsonify({
        'service': 'MCP Server - Weather API Wrapper',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check',
            '/tools': 'List available tools',
            '/call': 'Call a tool (JSON-RPC 2.0)'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': request.path
    }), 404


if __name__ == '__main__':
    port = int(os.getenv('MCP_SERVER_PORT', 8001))
    logger.info(f"Starting MCP Server on port {port}")
    app.run(debug=True, port=port, host='0.0.0.0')
