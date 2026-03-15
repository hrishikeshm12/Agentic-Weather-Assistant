"""
Backend Flask application for Weather Agent
Serves the agent API and frontend
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import BACKEND_PORT, DEBUG

# Configure logging BEFORE importing agent to capture all logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
# Set root logger to INFO to capture all module logs
logging.getLogger().setLevel(logging.INFO)

from agent import create_agent, process_query
from prompts import get_example_queries

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

# Initialize agent on startup
try:
    agent = create_agent()
    logger.info("Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {str(e)}")
    agent = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if agent else 'unhealthy',
        'service': 'Backend Agent Server'
    }), 200 if agent else 500


@app.route('/query', methods=['POST'])
def query_agent():
    """
    Process a query through the agent

    Request body:
    {
        "query": "What's the weather in London?"
    }

    Response:
    {
        "response": "Agent's response",
        "success": true
    }
    """
    if not agent:
        return jsonify({
            'error': 'Agent not initialized',
            'success': False
        }), 500

    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query parameter',
                'success': False
            }), 400

        user_query = data['query'].strip()

        if not user_query:
            return jsonify({
                'error': 'Query cannot be empty',
                'success': False
            }), 400

        logger.info(f"Received query: {user_query}")

        # Process query through agent (returns dict with text + tool_calls)
        result = process_query(agent, user_query)

        return jsonify({
            'response': result['text'],
            'tool_calls': result.get('tool_calls', []),
            'success': True
        }), 200

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/examples', methods=['GET'])
def get_examples():
    """Get example queries for the frontend"""
    return jsonify({
        'examples': get_example_queries()
    }), 200


@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset the agent's conversation history"""
    if agent:
        agent.clear_history()
        logger.info("Conversation history cleared")
    return jsonify({'success': True, 'message': 'Conversation reset'}), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service information"""
    return jsonify({
        'service': 'Backend Agent Server',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check',
            '/query': 'Process a weather query (POST)',
            '/examples': 'Get example queries'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': request.path
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting Backend Agent Server on port {BACKEND_PORT}")
    app.run(debug=DEBUG, port=BACKEND_PORT, host='0.0.0.0')
