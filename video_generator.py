import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from datetime import datetime
from models import db, Pipeline

def pick_random_file(folder):
    files = [f for f in os.listdir(folder) if not f.startswith('.') and os.path.isfile(os.path.join(folder, f))]
    if not files:
        return None
    return os.path.join(folder, files[0])  # Hier wird immer die erste Datei genommen; du kannst random.choice(files) einsetzen

def generate_nature_video(pipeline_id):
    pipeline = Pipeline.query.get(pipeline_id)
    if not pipeline:
        return None

    # Status updaten: Startzeit und Status-Text
    pipeline.status_text = "🎬 Video wird erstellt..."
    pipeline.started_at = datetime.utcnow()
    db.session.commit()

    # Ordner für Audio / Video festlegen
    audio_folder = "media/audio"
    video_folder = "media/video"

    audio_path = pick_random_file(audio_folder)
    video_path = pick_random_file(video_folder)

    if not audio_path or not video_path:
        pipeline.status_text = "⚠️ Kein Audio oder Video gefunden"
        db.session.commit()
        return None

    # Ausgabe-Pfad definieren
    output_folder = "media/output"
    os.makedirs(output_folder, exist_ok=True)
    output_file = f"pipeline_{pipeline_id}.mp4"
    output_path = os.path.join(output_folder, output_file)

    # Video + Audio kombinieren
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path).set_duration(video_clip.duration)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        pipeline.status_text = f"❌ Fehler beim Rendern: {e}"
        db.session.commit()
        return None

    # Status updaten: Rendern abgeschlossen
    pipeline.video_path = output_path
    pipeline.status_text = "✅ Rendering abgeschlossen"
    db.session.commit()

    return output_path
