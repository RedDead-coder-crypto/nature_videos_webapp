import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main as main_blueprint

app = Flask(__name__)

# ### 1.1 Datenbank‐Konfiguration ###
# Lokales SQLite, in Render später evtl. eine Umgebungsvariable verwenden:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ### 1.2 Blueprint registrieren ###
app.register_blueprint(main_blueprint)

# ### 1.3 Tabellen erstellen (falls nicht vorhanden) ###
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Nur beim lokalen Testen:
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
