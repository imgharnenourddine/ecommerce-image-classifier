from backend import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'image'
    
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False, default='default.jpg')
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Clé étrangère : pointe vers la table 'user' colonne 'id'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # --- LA CORRECTION EST ICI ---
    # 1. 'Prediction' avec P Majuscule (Nom de la Classe)
    # 2. J'ai renommé 'prediction' en 'predictions' (pluriel) car une image peut en avoir plusieurs
    predictions = db.relationship('Prediction', backref='image_source', lazy=True)

    def __repr__(self):
        return f"Image(id={self.id}, '{self.image_path}')" 