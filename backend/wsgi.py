"""WSGI entrypoint for production servers (gunicorn)"""
import os
from main import create_app

env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == '__main__':
    # For local debugging
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
