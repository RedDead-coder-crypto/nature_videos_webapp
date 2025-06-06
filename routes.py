from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Pipeline
from video_generator import generate_nature_video

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    GET  /            → zeigt eine Liste aller Pipelines + Formular zum Anlegen
    POST /            → legt eine neue Pipeline an und leitet zurück zu GET /
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_pipe = Pipeline(name=name, status_text="⏳ Wartend...")
            db.session.add(new_pipe)
            db.session.commit()
        return redirect(url_for('main.index'))

    # beim GET: wir holen alle Pipelines aus der DB und zeigen sie im Template
    pipelines = Pipeline.query.order_by(Pipeline.id.desc()).all()
    return render_template('index.html', pipelines=pipelines)


@main.route('/init-db', methods=['GET'])
def init_db():
    """
    Einmaliger Aufruf → erstellt die Datenbanktabellen (db.create_all()) 
    und zeigt eine kurze Bestätigung.
    """
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"


@main.route('/pipeline/<int:pipe_id>', methods=['GET'])
def show_pipeline(pipe_id):
    """
    GET /pipeline/<id>  → zeigt Name, Status, Startzeit, Video‐Pfad (falls fertig)
    """
    pip = Pipeline.query.get_or_404(pipe_id)
    return render_template('show_pipeline.html', pipeline=pip)


@main.route('/pipeline/<int:pipe_id>/run', methods=['POST'])
def run_pipeline(pipe_id):
    """
    POST /pipeline/<id>/run → startet die Video‐Generierung (synchron oder asynchron).
    In diesem Beispiel direkt synchron (blockierend); 
    in Produktion würdet ihr das in einen Hintergrund‐Worker packen.
    """
    pip = Pipeline.query.get_or_404(pipe_id)
    if pip.status_text.startswith("⏳"):
        # Wir verhindern doppeltes Ausführen
        pip.status_text = "⏳ Wird gerade verarbeitet..."
        db.session.commit()
        generate_nature_video(pipe_id)
    return redirect(url_for('main.show_pipeline', pipe_id=pipe_id))
