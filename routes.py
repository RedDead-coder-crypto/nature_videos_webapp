from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Zeige alle Pipelines (funktioniert nur, wenn Tabelle existiert)
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/create', methods=['POST'])
def create():
    name = request.form.get('name', 'Unnamed')
    new_pipeline = Pipeline(
        name=name,
        status_text='Gestartet',
        started_at=datetime.utcnow()
    )
    db.session.add(new_pipeline)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/init-db')
def init_db():
    # Erstellt die Tabelle(n), falls noch nicht vorhanden
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"

@main.route('/pipeline/<int:pipeline_id>/run', methods=['POST'])
def run_pipeline(pipeline_id):
    # Beispielhafte Route, um eine Pipeline manuell zu starten.
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    pipeline.status_text = "🚀 Wird ausgeführt..."
    pipeline.started_at = datetime.utcnow()
    db.session.commit()
    # Hier würdest du z.B. generate_nature_video() und upload_to_youtube() aufrufen.
    return redirect(url_for('main.index'))
