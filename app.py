from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy-Instanz, die in models.py importiert wird
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Pfad zur SQLite-Datenbank im Projektverzeichnis
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy konfigurieren
    db.init_app(app)

    # Blueprint mit allen Routen registrieren
    from routes import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    # Zum lokalen Start: python app.py
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
