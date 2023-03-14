from home_music import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(90), nullable=False)

    processes_logs = db.relationship("ProcessLog", backref="user", lazy=True)


class ProcessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(90), nullable=False)
    dir_path = db.Column(db.String(90), nullable=False)
    music_links = db.Column(db.String(90), nullable=False)
    music_names = db.Column(db.String(90), nullable=False)
    was_canceled = db.Column(db.Boolean, nullable=False)
    error_occurred = db.Column(db.Boolean, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
