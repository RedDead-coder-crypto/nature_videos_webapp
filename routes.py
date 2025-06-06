from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from datetime import datetime
import os

# Importiere den Generator
from video_generator import generate_nature_video

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/create', methods=['POST'])
def create():
    name = request.form.get('name', 'Pipeline ohne Namen')
    new_pipeline = Pipeline(name=name, status_text='Wartend', started_at=None)
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

    # 1. Status auf „Video wird erstellt“ setzen
    pipeline.status_text = "🎬 Video wird erstellt…"
    pipeline.started_at = datetime.utcnow()
    db.session.commit()

    # 2. Video generieren
    video_path = generate_nature_video(pipeline_id)
    if not video_path:
        # Fehlermeldung in Status schreiben
        pipeline.status_text = "⚠️ Fehlgeschlagen: Keine Mediendateien."
        db.session.commit()
        return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

    # 3. Video-Pfad in der Datenbank speichern
    pipeline.video_path = video_path
    pipeline.status_text = "✅ Rendering abgeschlossen"
    db.session.commit()

    # Hinweis: YouTube-Upload kommt später – hier beenden wir erst einmal
    return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

@main.route('/init-db')
def init_db():
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"
