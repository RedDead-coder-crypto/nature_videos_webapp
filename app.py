from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Pipeline
from scheduler import schedule_all_jobs, scheduler
import json
from apscheduler.triggers.cron import CronTrigger
from scheduler import run_pipeline

app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy initialisieren
db.init_app(app)

@app.before_first_request
def initialize_app():
    db.create_all()
    schedule_all_jobs(app)

# Startseite: Liste aller Pipelines anzeigen
@app.route('/')
def index():
    pipelines = Pipeline.query.order_by(Pipeline.created_at.desc()).all()
    return render_template('index.html', pipelines=pipelines)

# Neue Pipeline anlegen
@app.route('/pipeline/new', methods=['GET', 'POST'])
def new_pipeline():
    if request.method == 'POST':
        name = request.form['name']
        ptype = request.form['type']
        schedule = request.form['schedule']
        settings_raw = request.form.get('settings')
        try:
            settings = json.loads(settings_raw) if settings_raw else {}
        except json.JSONDecodeError:
            flash('Einstellungen müssen gültiges JSON sein', 'danger')
            return redirect(url_for('new_pipeline'))

        pipe = Pipeline(name=name, type=ptype, schedule=schedule)
        pipe.set_settings(settings)
        db.session.add(pipe)
        db.session.commit()

        # Job für neue Pipeline anlegen
        cron_fields = schedule.split()
        if len(cron_fields) == 5:
            trigger = CronTrigger(
                minute=cron_fields[0],
                hour=cron_fields[1],
                day=cron_fields[2],
                month=cron_fields[3],
                day_of_week=cron_fields[4]
            )
            scheduler.add_job(
                func=run_pipeline,
                trigger=trigger,
                args=[pipe.id],
                id=str(pipe.id)
            )

        flash('Neue Pipeline erstellt', 'success')
        return redirect(url_for('index'))

    return render_template('pipeline_form.html', pipeline=None)

# Pipeline bearbeiten
@app.route('/pipeline/<int:pipe_id>/edit', methods=['GET', 'POST'])
def edit_pipeline(pipe_id):
    pipe = Pipeline.query.get_or_404(pipe_id)
    if request.method == 'POST':
        pipe.name = request.form['name']
        pipe.type = request.form['type']
        pipe.schedule = request.form['schedule']
        settings_raw = request.form.get('settings')
        try:
            settings = json.loads(settings_raw) if settings_raw else {}
            pipe.set_settings(settings)
        except json.JSONDecodeError:
            flash('Einstellungen müssen gültiges JSON sein', 'danger')
            return redirect(url_for('edit_pipeline', pipe_id=pipe.id))

        pipe.active = 'active' in request.form
        db.session.commit()

        # Alten Job entfernen (falls vorhanden) und neu anlegen, wenn aktiv
        try:
            scheduler.remove_job(str(pipe.id))
        except:
            pass

        if pipe.active:
            cron_fields = pipe.schedule.split()
            if len(cron_fields) == 5:
                trigger = CronTrigger(
                    minute=cron_fields[0],
                    hour=cron_fields[1],
                    day=cron_fields[2],
                    month=cron_fields[3],
                    day_of_week=cron_fields[4]
                )
                scheduler.add_job(
                    func=run_pipeline,
                    trigger=trigger,
                    args=[pipe.id],
                    id=str(pipe.id)
                )

        flash('Pipeline aktualisiert', 'success')
        return redirect(url_for('index'))

    return render_template('pipeline_form.html', pipeline=pipe)

# Pipeline-Details anzeigen
@app.route('/pipeline/<int:pipe_id>')
def show_pipeline(pipe_id):
    pipe = Pipeline.query.get_or_404(pipe_id)
    return render_template('pipeline_detail.html', pipeline=pipe)

# Pipeline manuell auslösen
@app.route('/pipeline/<int:pipe_id>/run', methods=['POST'])
def trigger_pipeline(pipe_id):
    run_pipeline(pipe_id)
    flash('Pipeline manuell gestartet', 'info')
    return redirect(url_for('show_pipeline', pipe_id=pipe_id))

# Pipeline löschen
@app.route('/pipeline/<int:pipe_id>/delete', methods=['POST'])
def remove_pipeline(pipe_id):
    pipe = Pipeline.query.get_or_404(pipe_id)
    try:
        scheduler.remove_job(str(pipe.id))
    except:
        pass
    db.session.delete(pipe)
    db.session.commit()
    flash('Pipeline gelöscht', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
