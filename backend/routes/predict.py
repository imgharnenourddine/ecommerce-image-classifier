import os
import secrets
import re
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend import db
from backend.models.prediction import Prediction 
from backend.models.image import Image

# Tentative d'import du classificateur
try:
    from backend.ai.classifier import predict_image
except ImportError:
    def predict_image(path): return "Erreur IA", 0.0

prediction = Blueprint('prediction', __name__)

def save_prediction_image(form_picture):
    """Sauvegarde l'image physique entière dans le dossier uploads"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder_path = os.path.join(backend_dir, 'uploads')
    os.makedirs(folder_path, exist_ok=True)
    
    full_path = os.path.join(folder_path, picture_fn)
    form_picture.save(full_path)
    return picture_fn, full_path

@prediction.route('/api/predict', methods=['POST'])
@login_required 
def predict():
    mode = request.args.get('mode', 'temp') 
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    
    file = request.files['file']

    try:
        if mode == "temp":
            # --- MODE TEMPORAIRE : Analyse d'une zone ---
            temp_fn = f"temp_{secrets.token_hex(4)}.jpg"
            temp_path = os.path.join(os.getcwd(), temp_fn)
            file.save(temp_path)
            
            label_predit, score_confiance = predict_image(temp_path)
            
            if os.path.exists(temp_path):
                os.remove(temp_path) 
                
            return jsonify({
                "resultat": label_predit,
                "confiance": float(score_confiance)
            }), 200

        elif mode == "final":
            # --- MODE FINAL : Enregistrement de l'image entière ---
            filename, _ = save_prediction_image(file)
            
            final_labels = request.form.get('final_labels', 'Inconnu')
            final_confs_str = request.form.get('final_confs', '0%')

            # Calcul d'une confiance moyenne pour le Dashboard
            try:
                scores = [float(s) for s in re.findall(r"(\d+\.\d+)%", final_confs_str)]
                avg_conf = (sum(scores) / len(scores) / 100) if scores else 0.0
            except:
                avg_conf = 0.0

            # 1. Sauvegarde de l'image
            new_image = Image(user_id=current_user.id, image_path=filename)
            db.session.add(new_image)
            db.session.flush() # Récupère l'ID
            
            # 2. Sauvegarde de la prédiction groupée
            new_prediction = Prediction(
                image_id=new_image.id,         
                predicted_label=final_labels,
                confidence=avg_conf,
                model="ResNet50_Multi",
                
            )
            db.session.add(new_prediction)
            db.session.commit()

            return jsonify({"status": "success", "message": "Analyse enregistrée"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500