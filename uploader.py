from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from models import db, Pipeline
import os

def upload_to_youtube(pipeline_id, creds_json_path):
    """
    Lädt das gerenderte Video zur YouTube hoch.
    - pipeline_id: ID der Pipeline in der DB
    - creds_json_path: Pfad zur JSON-Datei mit YouTube OAuth-Credentials
    """
    pipeline = Pipeline.query.get(pipeline_id)
    if not pipeline or not pipeline.video_path:
        return None

    pipeline.status_text = "⬆️ Upload zu YouTube läuft..."
    db.session.commit()

    # Credentials laden (speichere deine YouTube OAuth2-Token in creds_json_path)
    creds = Credentials.from_authorized_user_file(creds_json_path, ["https://www.googleapis.com/auth/youtube.upload"])
    youtube = build("youtube", "v3", credentials=creds)

    # Request-Body definieren
    request_body = {
        'snippet': {
            'title': pipeline.name,
            'description': 'Automatisch generiertes Natur-Video',
            'tags': ['nature', 'relaxation', 'ambient'],
            'categoryId': '22'  # Kategorie: People & Blogs
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media_file = MediaFileUpload(pipeline.video_path, chunksize=-1, resumable=True)
    try:
        response_upload = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()
        video_id = response_upload.get("id")
        youtube_url = f"https://youtu.be/{video_id}"
    except Exception as e:
        pipeline.status_text = f"❌ Upload-Fehler: {e}"
        db.session.commit()
        return None

    # Status updaten: Upload abgeschlossen
    pipeline.youtube_url = youtube_url
    pipeline.status_text = "✅ Fertig hochgeladen"
    db.session.commit()

    return youtube_url
