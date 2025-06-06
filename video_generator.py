import os
from moviepy.editor import ColorClip

def generate_nature_video(pipeline_id: int, output_folder: str) -> str:
    """
    Erzeugt einen 5-Sekunden-Video-Clip (schwarz) und speichert ihn
    unter: <output_folder>/pipeline_<pipeline_id>.mp4
    Gibt den Dateinamen (ohne Pfad) zurück.
    """
    duration = 5  # Sekunden
    width, height = 1280, 720

    # Dateiname
    filename = f'pipeline_{pipeline_id}.mp4'
    output_path = os.path.join(output_folder, filename)

    # Ordner anlegen, falls er nicht existiert
    os.makedirs(output_folder, exist_ok=True)

    # Einfarbigen Clip (schwarz) erstellen
    clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=duration)
    clip = clip.set_fps(24)

    # Schreibe das Video (ohne Audio)
    clip.write_videofile(output_path, codec='libx264', audio=False, verbose=False, logger=None)

    return filename
