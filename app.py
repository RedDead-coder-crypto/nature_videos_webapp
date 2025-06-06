from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import main as main_blueprint

app = Flask(__name__)

# Datenbank-Konfiguration (lokal oder bei Render)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisiere Datenbank
db.init_app(app)

# Registriere Blueprint (aus routes.py)
app.register_blueprint(main_blueprint)

# Stelle sicher, dass das App-Objekt existiert für gunicorn
if __name__ == "__main__":
    app.run(debug=True)
