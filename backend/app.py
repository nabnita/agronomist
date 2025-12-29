"""
AgroMind AI - Flask Application
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from config import Config
from routes.api_routes import api

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure CORS to allow file:// protocol (for local HTML files)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # Allow all origins including file://
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": False
        }
    })
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Root route
    @app.route('/')
    def index():
        return {
            'service': 'AgroMind AI',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'predict': '/api/predict',
                'explain': '/api/explain',
                'ai_advice': '/api/ai-advice',
                'soil_impact': '/api/soil-impact',
                'crops': '/api/crops',
                'health': '/api/health'
            }
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

def main():
    """Run the application"""
    print("🌱 AgroMind AI - Starting Server")
    print("=" * 60)
    
    # Create app
    app = create_app()
    
    # Run server
    print(f"✓ Server running on http://localhost:{Config.PORT}")
    print(f"✓ Debug mode: {Config.DEBUG}")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )

if __name__ == '__main__':
    main()
