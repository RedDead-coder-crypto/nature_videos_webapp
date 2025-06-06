from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# db-Instanz wird durch app.py initialisiert
db = SQLAlchemy()

class Pipeline(db.Model):
    __tablename__ = 'pipeline'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    video_path = db.Column(db.String(200), nullable=True)
    youtube_url = db.Column(db.String(300), nullable=True)
    status_text = db.Column(db.String(100), nullable=False, default='Wartend …')
    started_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Pipeline {self.id} – {self.name}>'
