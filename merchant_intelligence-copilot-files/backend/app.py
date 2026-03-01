"""
Flask application for Merchant Intelligence Copilot
Converts AWS Lambda handlers to Flask routes for Render deployment
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os
import json

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from handlers import health, chat, generate_insights, weekly_report

app = Flask(__name__)
CORS(app)

def lambda_to_flask(handler_func):
    """Convert Lambda handler to Flask response"""
    try:
        # Build Lambda-style event from Flask request
        event = {
            'body': request.get_data(as_text=True) if request.data else '{}',
            'headers': dict(request.headers),
            'httpMethod': request.method,
            'path': request.path
        }
        
        # Call Lambda handler
        response = handler_func(event, None)
        
        # Convert Lambda response to Flask response
        status_code = response.get('statusCode', 200)
        body = response.get('body', '{}')
        headers = response.get('headers', {})
        
        # Parse body if it's a JSON string
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                pass
        
        flask_response = jsonify(body)
        flask_response.status_code = status_code
        
        for key, value in headers.items():
            if key.lower() not in ['content-type', 'content-length']:
                flask_response.headers[key] = value
            
        return flask_response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return lambda_to_flask(health.lambda_handler)

@app.route('/generate-insights', methods=['POST', 'OPTIONS'])
def generate_insights_route():
    if request.method == 'OPTIONS':
        return '', 204
    return lambda_to_flask(generate_insights.lambda_handler)

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat_route():
    if request.method == 'OPTIONS':
        return '', 204
    return lambda_to_flask(chat.lambda_handler)

@app.route('/weekly-report', methods=['POST', 'OPTIONS'])
def weekly_report_route():
    if request.method == 'OPTIONS':
        return '', 204
    return lambda_to_flask(weekly_report.lambda_handler)

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'Merchant Intelligence Copilot API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'generate_insights': '/generate-insights',
            'chat': '/chat',
            'weekly_report': '/weekly-report'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
