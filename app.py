from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipelines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importiere das Modell nach dem Initialisieren von db
from models import Pipeline

# Registriere Blueprint
app.register_blueprint(main)

# Erstelle die Datenbank (falls nicht vorhanden)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
