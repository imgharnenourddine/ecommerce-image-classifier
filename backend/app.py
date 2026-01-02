from flask import Flask
from backend.blueprints.api import api

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app
