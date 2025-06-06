from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pipeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    video_path = db.Column(db.String(200))
    youtube_url = db.Column(db.String(200))
    status_text = db.Column(db.String(255), default="Wartend")
    started_at = db.Column(db.DateTime, nullable=True)
