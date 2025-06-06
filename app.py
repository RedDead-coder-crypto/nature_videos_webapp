from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipelines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importiere das Modell, damit SQLAlchemy weiß, welche Tabellen es anlegen soll
from models import Pipeline

# Registriere den Blueprint für alle Routen
app.register_blueprint(main)

# Lege beim Start alle noch fehlenden Tabellen an
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
