from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Pipeline
from scheduler import schedule_all_jobs, scheduler
import json

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

        # Job direkt hinzufügen
        from apscheduler.triggers.cron import CronTrigger
        from scheduler import run_pipeline
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

# Pipeline bearbeiten, löschen, Details etc. (füge später zurück)
# ...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
