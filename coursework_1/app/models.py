from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True, unique=True)
    description = db.Column(db.String(500), index=True, unique=True, nullable=True)
    date = db.Column(db.Date())
    completed = db.Column(db.Boolean)
    dateCompleted = db.Column(db.Date())

    def __repr__(self):
        return '%s, %s, %s, %s, %s, %s' % (self.id, self.title, self.description, self.date, self.completed, self.dateCompleted)
