import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from models import db, Pipeline

# Standard-Ordnernamen (passen Sie diese Pfade an, falls Ihr Ordner anders heißt)
AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'media', 'audio')
VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'media', 'video')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output_videos')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_nature_video(pipeline_id: int):
    """
    1. Holt sich Pipeline aus der DB.
    2. Sucht sich alle Audio‐Dateien im AUDIO_DIR.
    3. Sucht sich Videoclips im VIDEO_DIR.
    4. Macht ein einfaches Zusammensetzen (z. B. erst alle Videos, dann Audio drüber).
    5. Speichert das Ergebnis unter output_videos/<pipeline_id>.mp4
    6. Aktualisiert Pipeline.status_text und video_path in der DB.
    """
    pip = Pipeline.query.get(pipeline_id)
    if pip is None:
        return

    pip.started_at = datetime.utcnow()
    db.session.commit()

    # 1. Audiodateien sammeln
    audios = []
    for filename in os.listdir(AUDIO_DIR):
        if filename.lower().endswith((".mp3", ".wav")):
            audios.append(os.path.join(AUDIO_DIR, filename))

    # 2. Videoclips sammeln
    videos = []
    for filename in os.listdir(VIDEO_DIR):
        if filename.lower().endswith((".mp4", ".mov", ".avi")):
            videos.append(os.path.join(VIDEO_DIR, filename))

    if not audios or not videos:
        # Kein Audio oder keine Videos = Fehler
        pip.status_text = "⚠ Fehlgeschlagen: Keine Mediendateien."
        db.session.commit()
        return

    # Beispiel‐Logik: alle VideoClips nacheinander zusammenfügen
    clips = [VideoFileClip(v) for v in videos]
    final_video = concatenate_videoclips(clips, method="compose")

    # Beispiel: nehmen die erste Audiodatei als Hintergrund‐Audio
    audio_clip = AudioFileClip(audios[0])
    final_video = final_video.set_audio(audio_clip)

    # Speichern unter output_videos/<pipeline_id>.mp4
    output_path = os.path.join(OUTPUT_DIR, f"{pipeline_id}.mp4")
    final_video.write_videofile(output_path, fps=24)

    # Status‐Update
    pip.video_path = output_path
    pip.status_text = "✔ Fertig: Video erzeugt."
    db.session.commit()
