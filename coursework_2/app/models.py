from app import db
from datetime import date


owns = db.Table('owns',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(64))
    password_last_update = db.Column(db.Date, default=date.today())
    email = db.Column(db.String(255), index=True, unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    owns = db.relationship('Book', secondary=owns, lazy='subquery', backref=db.backref('user', lazy=True))

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        """Perhaps add account locking features later"""
        return True

    def is_anonymous(self):
        """Perhaps add anonymous user functionality later"""
        return False

    def get_id(self):
        """Need to convert user identifier to Unicode value"""
        return self.username

    def __repr__(self):
        return "%s %s %s" % (self.id, self.username, self.email)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    author = db.Column(db.String(255), index=True)
    image = db.Column(db.String(512), default=None)
    description = db.Column(db.String(512), default=None)
    release_date = db.Column(db.Date, default=None)
    reviews = db.relationship('Review', backref='book', lazy='dynamic')

    def __repr__(self):
        return "%s %s %s %s" % (self.id, self.title, self.author, self.release_date)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)

    def __repr__(self):
        return "%s %s %s %s %s" % (self.id, self.rating, self.comment, self.user_id, self.book_id)



