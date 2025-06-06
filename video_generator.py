import os
import random
import subprocess
from datetime import datetime
from config import Config
import uuid

# Pfade aus Config
AUDIO_DIR = Config.AUDIO_DIR
VIDEO_DIR = Config.VIDEO_DIR
OUTPUT_DIR = Config.VIDEO_OUTPUT_DIR
VIDEO_LENGTH = Config.VIDEO_LENGTH

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def pick_random_file(directory, extensions):
    candidates = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and os.path.splitext(f)[1].lower() in extensions
    ]
    if not candidates:
        raise FileNotFoundError(f"Keine Dateien in {directory} mit Erweiterungen {extensions}")
    return os.path.join(directory, random.choice(candidates))

def generate_nature_video(settings):
    ensure_output_dir()
    length = settings.get('length_sec', VIDEO_LENGTH)
    audio_file = pick_random_file(AUDIO_DIR, ['.mp3', '.wav'])
    visual_file = pick_random_file(VIDEO_DIR, ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi'])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    output_name = f"nature_{timestamp}_{unique_id}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_name)
    _, vis_ext = os.path.splitext(visual_file)
    vis_ext = vis_ext.lower()
    if vis_ext in ['.jpg', '.jpeg', '.png']:
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', visual_file,
            '-i', audio_file,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-t', str(length),
            output_path
        ]
    else:
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', visual_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        vis_len = float(probe.stdout.strip())
        loops = int(length // vis_len) + 1
        concat_list = os.path.join(OUTPUT_DIR, f"concat_{unique_id}.txt")
        with open(concat_list, 'w') as f:
            f.write('ffconcat version 1.0\n')
            for _ in range(loops):
                f.write(f"file '{visual_file}'\n")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-i', concat_list,
            '-i', audio_file,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-t', str(length),
            output_path
        ]
    print("Erstelle Video mit Befehl:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    if vis_ext not in ['.jpg', '.jpeg', '.png']:
        os.remove(concat_list)
    return output_path

def generate_video_for_pipeline(pipeline):
    settings = pipeline.get_settings()
    if pipeline.type == 'nature':
        return generate_nature_video(settings)
    else:
        raise ValueError(f"Unbekannter Pipeline-Typ: {pipeline.type}")
