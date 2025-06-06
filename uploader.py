import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions
from config import Config

youtube_scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def get_youtube_service():
    creds = None
    token_pickle = Config.YOUTUBE_TOKEN_PICKLE
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except google.auth.exceptions.RefreshError:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.YOUTUBE_CLIENT_SECRETS_FILE, youtube_scopes
            )
            creds = flow.run_console()
        with open(token_pickle, 'wb') as f:
            pickle.dump(creds, f)
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path, pipeline):
    youtube = get_youtube_service()
    length_min = int(Config.VIDEO_LENGTH / 60)
    title = Config.TITLE_TEMPLATE.format(length_min=length_min)
    description = Config.DESCRIPTION_TEMPLATE.format(length_min=length_min)
    tags = Config.TAGS

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload-Status: {(status.progress() * 100):.2f}%")
    print("Upload abgeschlossen, Video-ID:", response.get('id'))
    return response.get('id')
