def generate_nature_video(pipeline_id):
    print(f"[DEBUG] Video-Generierung gestartet für Pipeline {pipeline_id}")
    audio_path = pick_random_file("media/audio")
    video_path = pick_random_file("media/video")
    print(f"[DEBUG] Audio gewählt: {audio_path}")
    print(f"[DEBUG] Video gewählt: {video_path}")

    if not audio_path or not video_path:
        print("[ERROR] Kein Audio oder Video gefunden!")
        return None
