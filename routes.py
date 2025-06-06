import os
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for

from models import db, Pipeline
from video_generator import generate_nature_video

main = Blueprint('main', __name__)

# Ordner, in dem die Videos gespeichert werden (relativ zum Projektstamm)
VIDEO_FOLDER = os.path.join('static', 'media', 'videos')

@main.route('/init-db')
def init_db():
    """
    Einmalig aufrufen, um die Datenbanktabelle 'pipeline' anzulegen.
    """
    db.create_all()
    return 'Datenbank (Tabelle „pipeline“) wurde angelegt.', 200

@main.route('/', methods=['GET'])
def index():
    """
    Zeigt das Formular zum Anlegen einer neuen Pipeline und listet alle Pipelines auf.
    """
    pipelines = Pipeline.query.order_by(Pipeline.id.desc()).all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/create', methods=['POST'])
def create_pipeline():
    """
    Legt eine neue Pipeline mit status_text='Wartend …' an.
    Leitet zurück zur Übersicht.
    """
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('main.index'))

    new_pipe = Pipeline(name=name, status_text='Wartend …')
    db.session.add(new_pipe)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/pipeline/<int:pipe_id>', methods=['GET'])
def show_pipeline(pipe_id):
    """
    Detailseite für eine einzelne Pipeline.
    Zeigt Name, Status, evtl. Video und YouTube-URL.
    """
    pip = Pipeline.query.get_or_404(pipe_id)
    return render_template('show_pipeline.html', pip=pip)

@main.route('/pipeline/<int:pipe_id>/run', methods=['POST'])
def run_pipeline(pipe_id):
    """
    Wird ausgeführt, wenn in der Detailseite auf „Pipeline ausführen“ geklickt wird.
    Setzt status_text = 'In Bearbeitung …', startet im Hintergrund
    die Video-Erzeugung und leitet zurück zur Detailseite.
    """
    pip = Pipeline.query.get_or_404(pipe_id)

    # Nur starten, wenn noch nicht begonnen (Status 'Wartend …')
    if pip.status_text != 'Wartend …':
        return redirect(url_for('main.show_pipeline', pipe_id=pipe_id))

    # Status aktualisieren
    pip.status_text = 'In Bearbeitung …'
    pip.started_at = datetime.utcnow()
    db.session.commit()

    # Hintergrund-Thread für Video-Erzeugung
    def background_job(pipeline):
        video_filename = generate_nature_video(pipeline.id, VIDEO_FOLDER)
        pipeline.video_path = os.path.join(VIDEO_FOLDER, video_filename)
        pipeline.status_text = 'Fertig ✓'
        db.session.commit()

    thread = threading.Thread(target=background_job, args=(pip,))
    thread.start()

    return redirect(url_for('main.show_pipeline', pipe_id=pipe_id))
