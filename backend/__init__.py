
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)    
loginmanager=LoginManager(app)
bcrypt=Bcrypt()

@loginmanager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": "Non autorisé",
        "message": "Veuillez vous connecter pour accéder à cette ressource."
    }), 401

from backend.models import user, image, prediction
from backend.routes.auth import auth
from backend.routes.predict import predict
from backend.routes.dashboard import dashboard
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(predict, url_prefix='/api/predict')
app.register_blueprint(dashboard, url_prefix='/api/dashboard')

