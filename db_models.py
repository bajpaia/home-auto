from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=False, nullable = False)
    email = db.Column(db.String(120), index=True, unique=True, nullable= False)
    password_hash = db.Column(db.String(128), nullable = False)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)  
