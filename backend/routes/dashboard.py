from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from backend import db
from backend.models.user import User
from backend.models.image import Image
from backend.models.prediction import Prediction

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/user/stats', methods=['GET'])
@login_required
def user_stats():
    user_id = current_user.id
    total_scans = Image.query.filter_by(user_id=user_id).count()
    user_predictions = db.session.query(Prediction).join(Image).filter(Image.user_id == user_id).all()
    
    avg_confidence = 0.0
    top_category = "None"
    
    if user_predictions:
        total_conf = sum(p.confidence for p in user_predictions)
        # CORRECTION : On renvoie la valeur brute (ex: 0.85) 
        # Le frontend Streamlit s'occupera du formatage %
        avg_confidence = round(total_conf / len(user_predictions), 4) 
        
        categories = [p.predicted_label for p in user_predictions]
        top_category = max(set(categories), key=categories.count)

    return jsonify({
        "username": current_user.username,
        "total_scans": total_scans,
        "avg_confidence": avg_confidence,
        "top_category": top_category
    }), 200

@dashboard.route('/user/history', methods=['GET'])
@login_required
def user_history():
    results = db.session.query(Image, Prediction)\
        .join(Prediction, Prediction.image_id == Image.id)\
        .filter(Image.user_id == current_user.id)\
        .order_by(Image.uploaded_at.desc())\
        .all()

    history_data = []
    for img, pred in results:
        # Statut basé sur la confiance brute
        if pred.confidence > 0.8: status = "Success"
        elif pred.confidence > 0.5: status = "Uncertain"
        else: status = "Failed"

        history_data.append({
            "id": img.id,
            "date": img.uploaded_at.strftime("%Y-%m-%d %H:%M"),
            "image_path": img.image_path, # Gardé pour construire l'URL dans Streamlit
            "category": pred.predicted_label,
            "confidence": round(pred.confidence, 4), # Valeur brute (ex: 0.8472)
            "status": status
        })

    return jsonify(history_data), 200

@dashboard.route('/admin/global-stats', methods=['GET'])
@login_required
def admin_global_stats():
    """
    Renvoie les statistiques de TOUS les utilisateurs confondus.
    """
    # Sécurité : Vérifier si c'est un admin
    if not getattr(current_user, 'is_admin', False):
        return jsonify({"error": "Access denied"}), 403

    total_users = User.query.count()
    total_predictions = Prediction.query.count()
    
    class_stats = db.session.query(
        Prediction.predicted_label, 
        func.count(Prediction.id)
    ).group_by(Prediction.predicted_label).all()
    
    # Formatage pour le frontend : {"Chat": 10, "Chien": 5}
    distribution = {label: count for label, count in class_stats}

    return jsonify({
        "total_users": total_users,
        "total_predictions": total_predictions,
        "class_distribution": distribution
    }), 200


@dashboard.route('/admin/users-list', methods=['GET'])
@login_required
def admin_users_list():
    """
    Renvoie la liste détaillée de tous les utilisateurs inscrits.
    """
    if not getattr(current_user, 'is_admin', False):
        return jsonify({"error": "Access denied"}), 403

    users = User.query.all()
    users_data = []

    for u in users:
        # On compte combien d'images chaque user a envoyé
        scan_count = Image.query.filter_by(user_id=u.id).count()
        
        users_data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": "Admin" if u.is_admin else "User",
            "total_scans": scan_count
        })

    return jsonify(users_data), 200