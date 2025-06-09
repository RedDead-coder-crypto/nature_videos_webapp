import os
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from video_generator import generate_nature_video

main = Blueprint('main', __name__)

# Wo die Videos abgelegt werden
VIDEO_FOLDER = os.path.join('static', 'media', 'videos')

# Hintergrund-Thread für Videoerzeugung
def run_pipeline(pipeline_id):
    pipeline = Pipeline.query.get(pipeline_id)
    pipeline.status_text = "In Bearbeitung …"
    pipeline.started_at = datetime.utcnow()
    db.session.commit()

    # Ordner anlegen, falls nicht vorhanden
    os.makedirs(VIDEO_FOLDER, exist_ok=True)

    # Video erzeugen
    filename = generate_nature_video(pipeline_id, VIDEO_FOLDER)

    # Datenbank aktualisieren
    pipeline.video_path = os.path.join(VIDEO_FOLDER, filename)
    pipeline.status_text = "Video erstellt ✓"
    db.session.commit()

# Datenbank initialisieren
@main.route('/init-db')
def init_db():
    db.create_all()
    return "Datenbank (Tabelle „pipeline“) wurde angelegt."

# Startseite mit Formular & Liste
@main.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

# Neue Pipeline anlegen
@main.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    pipeline = Pipeline(name=name)
    db.session.add(pipeline)
    db.session.commit()
    return redirect(url_for('main.index'))

# Detailansicht einer Pipeline
@main.route('/pipeline/<int:pipeline_id>')
def show_pipeline(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    return render_template('show_pipeline.html', pipeline=pipeline)

# Pipeline ausführen (Button klick)
@main.route('/pipeline/<int:pipeline_id>/run', methods=['POST'])
def run(pipeline_id):
    thread = threading.Thread(target=run_pipeline, args=(pipeline_id,))
    thread.daemon = True
    thread.start()
    return redirect(url_for('main.show_pipeline', pipeline_id=pipeline_id))
