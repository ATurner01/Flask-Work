from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(255), index=True, unique=True)
    authenticated = db.Column(db.Boolean, default=False)

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


