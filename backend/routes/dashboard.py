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
    """
    Renvoie les statistiques UNIQUEMENT pour l'utilisateur connecté.
    """
    user_id = current_user.id
    
    # 1. Nombre total d'images analysées par CE user
    total_scans = Image.query.filter_by(user_id=user_id).count()
    
    # 2. Récupérer toutes les prédictions de CE user pour calculer la confiance moyenne
    # Jointure : Prediction -> Image (filtré par user_id)
    user_predictions = db.session.query(Prediction).join(Image).filter(Image.user_id == user_id).all()
    
    avg_confidence = 0.0
    top_category = "Aucune"
    
    if user_predictions:
        # Calcul Moyenne Confiance
        total_conf = sum(p.confidence for p in user_predictions)
        avg_confidence = round((total_conf / len(user_predictions)) * 100, 1) # En pourcentage
        
        # Trouver la catégorie la plus fréquente
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
    """
    Renvoie la liste complète des prédictions de l'utilisateur (Historique).
    """
    # On récupère Image + Prediction, trié par date (le plus récent en premier)
    results = db.session.query(Image, Prediction)\
        .join(Prediction, Prediction.image_id == Image.id)\
        .filter(Image.user_id == current_user.id)\
        .order_by(Image.uploaded_at.desc())\
        .all()

    history_data = []
    for img, pred in results:
        # On détermine un statut visuel basé sur la confiance
        conf_percent = pred.confidence * 100
        if conf_percent > 80: status = "Succès"
        elif conf_percent > 50: status = "Incertain"
        else: status = "Échec"

        history_data.append({
            "id": img.id,
            "date": img.uploaded_at.strftime("%Y-%m-%d %H:%M"),
            "image_name": img.image_path,
            "category": pred.predicted_label,
            "confidence": round(conf_percent, 2),
            "status": status,
            "image_url": f"uploads/{img.image_path}" # Pour affichage éventuel
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
        return jsonify({"error": "Accès interdit"}), 403

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
        return jsonify({"error": "Accès interdit"}), 403

    users = User.query.all()
    users_data = []

    for u in users:
        # On compte combien d'images chaque user a envoyé
        scan_count = Image.query.filter_by(user_id=u.id).count()
        
        users_data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": "Admin" if u.is_admin else "Utilisateur",
            "total_scans": scan_count
        })

    return jsonify(users_data), 200