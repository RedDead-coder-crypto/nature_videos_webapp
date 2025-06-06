import os
from moviepy.editor import VideoFileClip, AudioFileClip

def generate_nature_video(pipeline_id):
    """
    Kombiniert media/video/sample.mp4 mit media/audio/sample.mp3
    und speichert das Ergebnis unter media/output_<pipeline_id>.mp4.
    Gibt den Pfad zur neuen Datei zurück oder None bei Fehler.
    """
    # Ordner- und Dateinamen festlegen
    base_dir = os.getcwd()
    audio_dir = os.path.join(base_dir, 'media', 'audio')
    video_dir = os.path.join(base_dir, 'media', 'video')
    output_dir = os.path.join(base_dir, 'media')

    audio_file = os.path.join(audio_dir, 'sample.mp3')
    video_file = os.path.join(video_dir, 'sample.mp4')
    output_file = os.path.join(output_dir, f'output_{pipeline_id}.mp4')

    # Überprüfen, ob die Quelldateien existieren
    if not os.path.exists(audio_file) or not os.path.exists(video_file):
        print(f"[WARN] Fehlende Quelldateien: {audio_file} oder {video_file}")
        return None

    try:
        # Video-Clip laden (wir nehmen die komplette Länge)
        video_clip = VideoFileClip(video_file)

        # Audio-Clip laden und auf die Länge des Videos trimmen
        audio_clip = AudioFileClip(audio_file).subclip(0, min(video_clip.duration, AudioFileClip(audio_file).duration))

        # Den Audio-Clip auf das Video legen
        final_clip = video_clip.set_audio(audio_clip)

        # Als neue Datei speichern
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', verbose=False, logger=None)

        print(f"[INFO] Video generiert: {output_file}")
        return output_file

    except Exception as e:
        print(f"[ERROR] Beim Generieren des Videos ist ein Fehler aufgetreten: {e}")
        return None
