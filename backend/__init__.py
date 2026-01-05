from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # J'utilise le nom standard snake_case
login_manager.login_view = 'auth.login'
from flask import send_from_directory
import os


@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    
    upload_path = os.path.join(app.root_path, 'uploads') 
    return send_from_directory(upload_path, filename)
CORS(app)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": "Non autorisé",
        "message": "Veuillez vous connecter pour accéder à cette ressource."
    }), 401

# --- C'EST ICI QU'ON BRISE LA BOUCLE ---
# On définit le user_loader ICI, pas dans models/user.py
@login_manager.user_loader
def load_user(user_id):
    # On fait l'import DANS la fonction pour éviter que ça bloque au démarrage
    from backend.models.user import User 
    return User.query.get(int(user_id))

# --- IMPORTS DES BLUEPRINTS (TOUT EN BAS) ---
# Ils doivent être importés APRÈS que 'db' et 'app' soient créés
from backend.routes.auth import auth
from backend.routes.predict import prediction
from backend.routes.dashboard import dashboard

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(prediction) # Vérifiez l'URL dans prediction.py
app.register_blueprint(dashboard, url_prefix='/api/dashboard')

# Création des tables
with app.app_context():
    db.create_all()