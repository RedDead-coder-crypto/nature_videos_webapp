from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from video_generator import generate_nature_video
from uploader import upload_to_youtube
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/pipeline/new', methods=['GET', 'POST'])
def new_pipeline():
    if request.method == 'POST':
        name = request.form['name']
        pipeline = Pipeline(name=name)
        db.session.add(pipeline)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('pipeline_new.html')

@main.route('/pipeline/<int:pipeline_id>')
def pipeline_detail(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    return render_template('pipeline_detail.html', pipeline=pipeline, datetime=datetime)

@main.route('/pipeline/<int:pipeline_id>/run', methods=['POST'])
def run_pipeline(pipeline_id):
    generate_nature_video(pipeline_id)
    pipeline = Pipeline.query.get(pipeline_id)
    upload_to_youtube(pipeline.video_path, pipeline_id)
    return redirect(url_for('main.pipeline_detail', pipeline_id=pipeline_id))
