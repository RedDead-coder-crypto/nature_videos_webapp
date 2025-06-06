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
        try:
            scheduler.remove_job(str(pipe.id))
        except:
            pass
        if pipe.active:
            from apscheduler.triggers.cron import CronTrigger
            from scheduler import run_pipeline
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

@app.route('/pipeline/<int:pipe_id>')
def show_pipeline(pipe_id):
    pipe = Pipeline.query.get_or_404(pipe_id)
    return render_template('pipeline_detail.html', pipeline=pipe)

@app.route('/pipeline/<int:pipe_id>/run', methods=['POST'])
def trigger_pipeline(pipe_id):
    from scheduler import run_pipeline
    run_pipeline(pipe_id)
    flash('Pipeline manuell gestartet', 'info')
    return redirect(url_for('show_pipeline', pipe_id=pipe_id))

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
