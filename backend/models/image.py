from backend import db
from datetime import datetime

class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    image_path=db.Column(db.String(255),nullable=False,default='default.jpg')
    uploaded_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    prediction=db.relationship('prediction',backref='image',lazy=True)
    def __repr__(self):
        return f"Image(id={self.id}, '{self.image_path}')"