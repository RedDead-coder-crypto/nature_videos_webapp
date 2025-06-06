from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Lies alle Pipelines aus der Datenbank
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
    # TEMPORÄR: Ändere nur den Status zum Testen, ohne Video-Logik
    pipeline.status_text = "✅ Test: Status hat sich geändert!"
    pipeline.started_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))

@main.route('/init-db')
def init_db():
    # Falls bei App-Start aus irgendeinem Grund create_all() nicht gegriffen hat,
    # kannst du hiermit manuell die Tabellen anlegen.
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"
