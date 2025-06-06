import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main as main_blueprint
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy an Flask binden
db.init_app(app)

# Blueprint registrieren
app.register_blueprint(main_blueprint)

# Tabelle anlegen, falls sie noch nicht existiert
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
