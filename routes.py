from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from video_generator import generate_nature_video
from uploader import upload_to_youtube
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/create', methods=['POST'])
def create():
    name = request.form.get('name', 'Pipeline ohne Namen')
    new_pipeline = Pipeline(
        name=name,
        status_text='Wartend',
        started_at=None
    )
    db.session.add(new_pipeline)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/pipeline/<int:pipeline_id>')
def pipeline_detail(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    return render_template('pipeline_detail.html', pipeline=pipeline)

@main.route('/pipeline/<int:pipeline_id>/run', methods=['POST'])
def run_pipeline(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)

    # 1. Video generieren
    video_path = generate_nature_video(pipeline_id)
    if not video_path:
        return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

    # 2. YouTube-Upload (credentials.json muss im Projekt liegen)
    creds_path = os.path.join(os.getcwd(), 'credentials.json')
    youtube_url = upload_to_youtube(pipeline_id, creds_path)
    if not youtube_url:
        return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

    return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

@main.route('/init-db')
def init_db():
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"
