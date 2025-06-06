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
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Datenbank wurde initialisiert.")
    app.run(debug=True)
# ganz oben
from flask import Blueprint
from models import db

main = Blueprint('main', __name__)

# Diese neue Route fügt die Tabelle hinzu!
@main.route('/init-db')
def init_db():
    db.create_all()
    return "Database initialized"
