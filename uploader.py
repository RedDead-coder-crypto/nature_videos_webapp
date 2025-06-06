from models import db, Pipeline

def upload_to_youtube(video_path, pipeline_id):
    pipeline = Pipeline.query.get(pipeline_id)

    # Simuliere Upload (z. B. Zeitverzögerung)
    import time
    time.sleep(5)

    # Setze Dummy-Link (oder hier YouTube-Upload-Code einbauen)
    pipeline.youtube_url = "https://youtube.com/dummyvideo"
    pipeline.status_text = "✅ Fertig hochgeladen"
    db.session.commit()
