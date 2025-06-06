from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
# Die Video-/Uploader-Imports kannst du jetzt temporär drinlassen, sie werden aber nicht genutzt.
from datetime import datetime

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
    # --- HIER IST NUR DER TESTCODE:
    pipeline.status_text = "✅ Test: Status hat sich geändert!"
    pipeline.started_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))
# --- Ende Testcode

@main.route('/init-db')
def init_db():
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"
