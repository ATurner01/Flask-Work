from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(255), index=True, unique=True)
