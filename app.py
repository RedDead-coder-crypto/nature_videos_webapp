from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Blueprints registrieren
app.register_blueprint(main)

# Datenbanktabellen erstellen (falls nicht vorhanden)
with app.app_context():
    db.create_all()
