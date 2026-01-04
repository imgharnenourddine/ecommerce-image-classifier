from backend import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'prediction'

    id = db.Column(db.Integer, primary_key=True)
    predicted_label = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clé étrangère : pointe vers la table 'image' colonne 'id'
    image_id = db.Column(db.Integer, db.ForeignKey('image.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Prediction('{self.predicted_label}', {self.confidence * 100}%)"