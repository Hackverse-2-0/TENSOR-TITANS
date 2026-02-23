"""PDS Leak Detection Platform - Main Application"""
import os
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import datetime

# Import configuration and models
from config import config
from models import db, UserRole

# Import API blueprints
from api.auth_routes import auth_bp
from api.data_routes import data_bp
from api.anomaly_routes import anomaly_bp
from api.shop_routes import shop_bp
from api.database_routes import db_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory"""
    
    app = Flask(__name__)
    # Allow serving frontend files when enabled in config
    serve_frontend = os.getenv('SERVE_FRONTEND', 'false').lower() in ('1', 'true', 'yes') or app.config.get('SERVE_FRONTEND', False)
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(anomaly_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(db_bp)
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        # Prevent caching of sensitive data
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data: https:; font-src 'self' https://cdnjs.cloudflare.com;"
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Feature Policy
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=()'
        
        return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200
    
    # Home endpoint
    @app.route('/', methods=['GET'])
    def home():
        # In production deployments we may want to serve the frontend
        if serve_frontend and os.path.isdir(frontend_dir):
            index_path = os.path.join(frontend_dir, 'login.html')
            if os.path.exists(index_path):
                return send_from_directory(frontend_dir, 'login.html')
        return jsonify({
            'name': 'PDS Leak Detection Platform',
            'version': '1.0.0',
            'description': 'Detect and prevent stock leaks in Public Distribution System',
            'endpoints': {
                'health': '/api/v1/health',
                'auth': '/api/v1/auth',
                'shops': '/api/v1/shops',
                'data_ingestion': '/api/v1/data',
                'anomalies': '/api/v1/anomalies'
            },
            'documentation': '/docs'
        }), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")

    # Serve frontend static files if requested (single-file catch-all)
    if serve_frontend and os.path.isdir(frontend_dir):
        @app.route('/<path:path>', methods=['GET'])
        def serve_frontend_files(path):
            # Prevent exposing sensitive backend files
            if path.startswith('backend') or path.endswith('.py'):
                return jsonify({'error': 'Not found'}), 404
            file_path = os.path.join(frontend_dir, path)
            if os.path.exists(file_path):
                return send_from_directory(frontend_dir, path)
            # fallback to login page for SPA-like behavior
            return send_from_directory(frontend_dir, 'login.html')
    
    return app

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    
    # Debug mode
    debug = env == 'development'
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug,
        use_reloader=debug
    )
