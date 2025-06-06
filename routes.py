from flask import Blueprint, render_template, request, redirect, url_for
from models import Pipeline, db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@main.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    new_pipeline = Pipeline(
        name=name,
        status_text='Gestartet',
        started_at=datetime.utcnow()
    )
    db.session.add(new_pipeline)
    db.session.commit()
    return redirect(url_for('main.index'))
