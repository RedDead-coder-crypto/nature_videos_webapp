import os
from moviepy.editor import ColorClip

# Erzeugt ein Dummy-Video (schwarzes Bild über Dauer)
def generate_nature_video(pipeline_id, output_folder):
    duration = 5  # Sekunden
    fps = 24
    clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=duration)
    filename = f'pipeline_{pipeline_id}.mp4'
    output_path = os.path.join(output_folder, filename)
    clip.write_videofile(output_path, fps=fps, codec="libx264", audio=False)
    return filename
