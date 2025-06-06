from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Pipeline
from scheduler import schedule_all_jobs, scheduler
import json

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_first_request
def initialize_app():
    # Tabelle anlegen, bevor der erste Request bedient wird
    db.create_all()
    # Hintergrund‐Scheduler starten
    schedule_all_jobs(app)

@app.route('/')
def index():
    pipelines = Pipeline.query.order_by(Pipeline.created_at.desc()).all()
    return render_template('index.html', pipelines=pipelines)

@app.route('/pipeline/new', methods=['GET', 'POST'])
def new_pipeline():
    # … (der Rest bleibt unverändert) …
    return render_template('pipeline_form.html', pipeline=None)

# … (alle anderen Routen unverändert) …

if __name__ == '__main__':
    # Dieser Block wird unter Gunicorn nicht ausgeführt,
    # kann aber fürs lokale Testing dort bleiben:
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
