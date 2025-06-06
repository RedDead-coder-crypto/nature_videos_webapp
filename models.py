from datetime import datetime

class Pipeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    status_text = db.Column(db.String(200), default="Wartet…")
    started_at = db.Column(db.DateTime, default=None)
