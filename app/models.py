from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    location = db.Column(db.String(128))
    api_key = db.Column(db.String(128), unique=True)
    users = db.relationship('User', backref='hospital', lazy='dynamic')

    def __repr__(self):
        return f'<Hospital {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_online(self):
        if self.last_seen is None:
            return False
        return (datetime.utcnow() - self.last_seen).total_seconds() < 120

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    details = db.Column(db.String(512))

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'

class ModelVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version_number = db.Column(db.Integer, unique=True)
    global_weights_path = db.Column(db.String(256))
    accuracy = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ModelVersion {self.version_number}>'
