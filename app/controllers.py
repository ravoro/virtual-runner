from flask import flash
from flask import url_for, redirect, render_template

from app import app, db
from .forms import JourneysAddForm, JourneysAddStageForm
from .models import Journey, Stage


@app.route('/')
def home():
    return redirect(url_for('journeys'))


@app.route('/journeys')
def journeys():
    journeys = Journey.query.all()
    return render_template('journeys.html', journeys=journeys)


@app.route('/journeys/add', methods=['GET', 'POST'])
def journeys_add():
    form = JourneysAddForm()
    if form.validate_on_submit():
        journey = Journey(
            name=str(form.name.data),
            start_lat=float(form.start_lat.data),
            start_lng=float(form.start_lng.data),
            finish_lat=float(form.finish_lat.data),
            finish_lng=float(form.finish_lng.data)
        )
        db.session.add(journey)
        db.session.commit()

        flash('Successfully created new journey.')
        return redirect(url_for('journey', jid=journey.id))
    return render_template('journeys_add.html', form=form)


@app.route('/journeys/<int:jid>')
def journey(jid):
    journey = Journey.query.get(jid)
    return render_template('journey.html', journey=journey)


@app.route('/journeys/<int:jid>/stages/add', methods=['GET', 'POST'])
def journeys_add_stage(jid):
    journey = Journey.query.get(jid)
    form = JourneysAddStageForm()
    if form.validate_on_submit():
        stage = Stage(
            distance=int(form.distance.data),
            journey=journey
        )
        db.session.add(stage)
        db.session.commit()

        flash('Successfully added new stage.')
        return redirect(url_for('journey', jid=journey.id))
    return render_template('journeys_add_stage.html', form=form)
