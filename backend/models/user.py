from backend import db,loginmanager
from datetime import datetime

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(25),nullable=False)
    lname=db.Column(db.String(25),nullable=False)
    username=db.Column(db.String(25),unique=True,nullable=False)
    email=db.Column(db.String(60),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    images=db.relationship('image',backref='proprietaire',lazy=True)
    def __repr__(self):
        return f'USER({self.fname},{self.lname},{self.username},{self.email})'