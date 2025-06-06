from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from models import db, Pipeline
from video_generator import generate_video_for_pipeline
from uploader import upload_to_youtube
from datetime import datetime

scheduler = BackgroundScheduler()

def schedule_all_jobs(app):
    with app.app_context():
        pipelines = Pipeline.query.filter_by(active=True).all()
        for pipe in pipelines:
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
    scheduler.start()

def run_pipeline(pipeline_id):
    from models import Pipeline
    pipe = Pipeline.query.get(pipeline_id)
    if not pipe or not pipe.active:
        return
    try:
        video_path = generate_video_for_pipeline(pipe)
        upload_to_youtube(video_path, pipe)
        pipe.last_run = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        print(f"Fehler bei Pipeline {pipeline_id}: {e}")
