from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipelines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Damit SQLAlchemy die Modelle kennt
from models import Pipeline

# Registriere unsere Routen (Blueprint)
app.register_blueprint(main)

# ERSTELLE DB im Startkontext (wenn init-db nicht explizit aufgerufen wird, sorgt das für Sicherheit)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
