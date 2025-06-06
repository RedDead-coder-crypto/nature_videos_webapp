from flask import Flask
from models import db, Pipeline  # Importiere SQLAlchemy-Instanz und Modell
from routes import main          # Importiere das Blueprint mit allen Routen

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipelines.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Binde SQLAlchemy an die App
    db.init_app(app)

    # Registriere das Blueprint
    app.register_blueprint(main)

    # Erzeuge beim Start sicher alle Tabellen, falls sie fehlen
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
