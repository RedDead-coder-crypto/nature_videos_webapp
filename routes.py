import os
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Pipeline
from video_generator import generate_nature_video, upload_to_youtube

main = Blueprint('main', __name__)

@main.route('/init-db', methods=['GET'])
def init_db():
    """
    Lädt einmalig die Datenbank und Tabelle 'pipeline'
    """
    db.create_all()
    return "✅ Datenbank und Tabelle 'pipeline' wurden erstellt!"

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    GET  /  → zeigt die Übersicht (Formular + Liste aller Pipelines)
    POST /  → legt eine neue Pipeline an und leitet zurück zu GET /
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_pipe = Pipeline(name=name, status_text
