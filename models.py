from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Instanz von SQLAlchemy
db = SQLAlchemy()

class Pipeline(db.Model):
    __tablename__ = 'pipelines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    schedule = db.Column(db.String(64), nullable=False)  # Cron-Expression
    active = db.Column(db.Boolean, default=True)
    settings = db.Column(db.Text, nullable=True)         # JSON-String für weitere Optionen
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_run = db.Column(db.DateTime, nullable=True)

    def get_settings(self):
        if self.settings:
            return json.loads(self.settings)
        return {}

    def set_settings(self, settings_dict):
        self.settings = json.dumps(settings_dict)

    def __repr__(self):
        return f"<Pipeline {self.id} - {self.name} ({self.type})>"
