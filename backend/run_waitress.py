"""Run the Flask app with Waitress server (production-like)"""
import os

# Ensure development config (sqlite) is used so DB exists in this workspace
# Set environment variables before importing the WSGI app so the correct
# configuration (development) is used during app creation.
os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
os.environ['SERVE_FRONTEND'] = 'true'

from waitress import serve
from wsgi import app as wsgi_app

if __name__ == '__main__':
    print('Starting Waitress server on 0.0.0.0:5000')
    serve(wsgi_app, host='0.0.0.0', port=5000, threads=4)
