import os
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from video_generator import generate_nature_video, upload_to_youtube

main = Blueprint('main', __name__)

@main.route('/init-db', methods=['GET'])
def init_db():
    """
    Lädt einmalig die Datenbank und Tabelle 'pipeline'
    """
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    GET  /  → zeigt die Übersicht (Formular + Liste aller Pipelines)
    POST /  → legt eine neue Pipeline an und leitet zurück zu GET /
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_pipe = Pipeline(name=name, status_text="⏳ Wartend...")
            db.session.add(new_pipe)
            db.session.commit()
        return redirect(url_for('main.index'))

    # Wenn hierher per GET navigiert wird:
    pipelines = Pipeline.query.order_by(Pipeline.id.desc()).all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/pipeline/<int:pipe_id>')
def show_pipeline(pipe_id):
    """
    Zeigt Detailseite für eine einzelne Pipeline
    """
    pip = Pipeline.query.get_or_404(pipe_id)
    return render_template('show_pipeline.html', pip=pip)

@main.route('/create', methods=['POST'])
def create_pipeline():
    """
    Wird ausgelöst, wenn im Formular auf 'Erstellen' geklickt wird.
    Leitet zurück auf '/'
    """
    name = request.form.get('name', '').strip()
    if name:
        new_pipe = Pipeline(name=name, status_text="⏳ Wartend...")
        db.session.add(new_pipe)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/pipeline/<int:pipe_id>/run', methods=['POST'])
def run_pipeline(pipe_id):
    """
    Startet im Hintergrund die Erzeugung und den Upload des Videos.
    """
    pip = Pipeline.query.get_or_404(pipe_id)
    pip.status_text = "🔄 In Bearbeitung..."
    pip.started_at = datetime.utcnow()
    db.session.commit()

    def background_task(pipeline_id):
        # Video erzeugen
        updated_pipe = Pipeline.query.get(pipeline_id)
        video_path = generate_nature_video(updated_pipe.id)
        updated_pipe.video_path = video_path
        updated_pipe.status_text = "🔼 Hochladen auf YouTube..."
        db.session.commit()

        # Auf YouTube hochladen
        youtube_url = upload_to_youtube(video_path, updated_pipe.id)
        updated_pipe.youtube_url = youtube_url
        updated_pipe.status_text = "✅ Fertig"
        db.session.commit()

    thread = threading.Thread(target=background_task, args=(pip.id,))
    thread.start()

    return redirect(url_for('main.show_pipeline', pipe_id=pipe_id))
