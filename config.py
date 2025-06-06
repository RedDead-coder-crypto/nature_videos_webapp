import os
from dotenv import load_dotenv

# Lade alle Umgebungsvariablen aus .env
load_dotenv()

class Config:
    # Flask-Konfiguration
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")

    # SQLAlchemy (hier SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///nature_videos.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # YouTube API
    YOUTUBE_CLIENT_SECRETS_FILE = os.environ.get("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    YOUTUBE_TOKEN_PICKLE = os.environ.get("YOUTUBE_TOKEN_PICKLE", "token_youtube_upload.pickle")

    # Mediathek-Ordner
    AUDIO_DIR = os.environ.get("AUDIO_DIR", "media/audio")
    VIDEO_DIR = os.environ.get("VIDEO_DIR", "media/video")
    VIDEO_OUTPUT_DIR = os.environ.get("VIDEO_OUTPUT_DIR", "output_videos")

    # Video-Metadaten (Templates)
    TITLE_TEMPLATE = os.environ.get(
        "TITLE_TEMPLATE",
        "Naturgeräusche – {length_min} Minuten Entspannung – Kein Text"
    )
    DESCRIPTION_TEMPLATE = os.environ.get(
        "DESCRIPTION_TEMPLATE",
        "Entspannende Naturgeräusche ({length_min} Minuten). Generiert automatisch.\\n#Natur #Entspannung #Ambient"
    )
    TAGS = [tag.strip() for tag in os.environ.get(
        "TAGS",
        "Naturgeräusche,Entspannung,Ambient,ASMR"
    ).split(",")]

    # Default-Länge für generierte Videos (in Sekunden)
    VIDEO_LENGTH = int(os.environ.get("VIDEO_LENGTH", "3600"))
