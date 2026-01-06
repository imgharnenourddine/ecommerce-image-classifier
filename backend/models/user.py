from backend import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user' # On force le nom de la table
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    images = db.relationship('Image', backref='proprietaire', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"