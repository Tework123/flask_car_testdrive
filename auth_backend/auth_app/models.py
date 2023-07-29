import base64
import os
from datetime import datetime, timedelta

from auth_app import db, login_manager


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    country = db.Column(db.String(50))
    password = db.Column(db.String(500))
    profile_pic = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now())
    phone = db.Column(db.String(100))
    text = db.Column(db.String(500), nullable=True)
    last_seen = db.Column(db.DateTime)
    last_seen_profile = db.Column(db.DateTime, default=datetime.now())
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id_user)

    def get_token(self, expires_in=15000):
        now = datetime.now()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Users.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.now():
            return None
        return user


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
