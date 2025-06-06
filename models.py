from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pipeline(db.Model):
    __tablename__ = 'pipeline'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    video_path = db.Column(db.String(256), nullable=True)
    youtube_url = db.Column(db.String(256), nullable=True)
    status_text = db.Column(db.String(128), nullable=True)
    started_at = db.Column(db.DateTime, nullable=True, default=None)

    def __repr__(self):
        return f'<Pipeline {self.id} {self.name}>'
