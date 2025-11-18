from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from routes import register_routes
from utils import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger()

# Create Flask app
app = Flask(__name__)

# Enable CORS
allowed_origins = os.getenv('FRONTEND_URL', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
app.config['PORT'] = int(os.getenv('PORT', 5000))

# Register routes
register_routes(app)

if __name__ == '__main__':
    port = app.config['PORT']
    debug = app.config['DEBUG']
    logger.info(f'Starting Flask application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)

