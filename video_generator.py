import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from datetime import datetime
from models import db, Pipeline

def generate_nature_video(pipeline_id):
    pipeline = Pipeline.query.get(pipeline_id)
    pipeline.status_text = "🎬 Video wird erstellt..."
    pipeline.started_at = datetime.utcnow()
    db.session.commit()

    base_dir = "media"
    video_file = os.path.join(base_dir, "video.mp4")
    audio_file = os.path.join(base_dir, "audio.mp3")

    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file).set_duration(video.duration)
    final = video.set_audio(audio)

    output_path = os.path.join(base_dir, f"output_{pipeline_id}.mp4")
    final.write_videofile(output_path, codec="libx264")

    pipeline.video_path = output_path
    pipeline.status_text = "⬆️ Video wird hochgeladen..."
    db.session.commit()
