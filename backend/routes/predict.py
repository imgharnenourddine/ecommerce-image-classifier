import os
import secrets
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend import db

from backend.models.prediction import Prediction 
from backend.models.image import Image

try:
    from backend.ai.classifier import predict_image
except ImportError:
    def predict_image(path): return "Erreur IA", 0.0

prediction = Blueprint('prediction', __name__)

def save_prediction_image(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    current_file = os.path.abspath(__file__)
    routes_dir = os.path.dirname(current_file)
    backend_dir = os.path.dirname(routes_dir)
    
    folder_path = os.path.join(backend_dir, 'uploads')
    
    os.makedirs(folder_path, exist_ok=True)
    
    full_path = os.path.join(folder_path, picture_fn)
    form_picture.save(full_path)
    
    return picture_fn, full_path


@prediction.route('/api/predict', methods=['POST'])
@login_required 
def predict():
    
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    try:
        
        filename, full_path = save_prediction_image(file)

        # On crée l'objet Image en premier
        new_image = Image(
            user_id=current_user.id,
            image_path=filename
            
        )
        
        
        db.session.add(new_image)
        db.session.commit()
        
        
        image_id_genere = new_image.id

        
        label_predit, score_confiance = predict_image(full_path)

       
        new_prediction = Prediction(
            image_id=image_id_genere,         
            predicted_label=str(label_predit),
            confidence=float(score_confiance),
            model="CNN_Model_v1"              
        )

        db.session.add(new_prediction)
        db.session.commit()

        
        return jsonify({
            "message": "Analyse réussie",
            "resultat": label_predit,
            "confiance": score_confiance,
            "image_id": image_id_genere,
            "image_filename": filename
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur serveur : {e}")
        return jsonify({"error": "Erreur interne", "details": str(e)}), 500