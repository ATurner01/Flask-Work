from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True, unique=True)
    description = db.Column(db.String(500), index=True, unique=True, nullable=True)
    completed = db.Column(db.Boolean)


