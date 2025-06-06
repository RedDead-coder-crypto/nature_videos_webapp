from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# **Nur hier** wird eine einzige SQLAlchemy-Instanz erstellt.
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # SQLite-Datenbank in der Projekt-Wurzel
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # binde unsere db-Instanz an diese App
    db.init_app(app)

    # registriere alle Routen (Blueprint)
    from routes import main
    app.register_blueprint(main)

    return app

# Nur für den lokalen Start: python app.py
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
