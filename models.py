from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # wir initialisieren es später in app.py

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    status_text = db.Column(db.String(256), nullable=True)
    video_path = db.Column(db.String(256), nullable=True)
    youtube_url = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"<Pipeline {self.id} – {self.name}>"
