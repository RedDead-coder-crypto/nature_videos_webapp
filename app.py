from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Datenbank-Extension initialisieren
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Blueprint-Registration
    from routes import main
    app.register_blueprint(main)

    return app

# WSGI-Entry-Point
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
