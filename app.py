from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Für Render: Umgebungsvariable DATABASE_URL (z.B. sqlite) -> hier local sqlite als Fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pipeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    settings = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/')
def index():
    pipelines = Pipeline.query.all()
    return render_template('index.html', pipelines=pipelines)

@app.route('/pipeline/new', methods=['GET', 'POST'])
def new_pipeline():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        schedule = request.form['schedule']
        settings_raw = request.form.get('settings')
        settings = settings_raw if settings_raw else ''
        active = True
        db.session.add(Pipeline(name=name, type=type_, schedule=schedule, settings=settings, active=active))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pipeline_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
