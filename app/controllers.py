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
    if form.is_submitted():
        if form.validate():
            journey = Journey(
                name=str(form.name.data),
                distance_meters=int(form.distance_meters.data),
                start_lat=float(form.start_lat.data),
                start_lng=float(form.start_lng.data),
                finish_lat=float(form.finish_lat.data),
                finish_lng=float(form.finish_lng.data)
            )
            db.session.add(journey)
            db.session.commit()

            flash('Successfully created new journey.')
            return redirect(url_for('journey', jid=journey.id))
        else:
            return render_template('journeys_add.html', form=form), 400
    return render_template('journeys_add.html', form=form)


@app.route('/journeys/<int:jid>')
def journey(jid):
    journey = Journey.query.get(jid)
    return render_template('journey.html', journey=journey)


@app.route('/journeys/<int:jid>/stages/add', methods=['GET', 'POST'])
def journeys_add_stage(jid):
    journey = Journey.query.get(jid)

    if journey.is_completed:
        flash('The journey has been completed.')
        return redirect(url_for('journey', jid=journey.id))

    form = JourneysAddStageForm()
    if form.is_submitted():
        if form.validate():
            # add stage to db
            stage = Stage(
                distance_meters=int(form.distance_meters.data),
                journey=journey
            )
            db.session.add(stage)
            db.session.commit()

            # determine if the journey has been completed
            if journey.is_completed:
                flash('Congratulations! You\'ve completed the journey. You can now make me burritos...')
                return redirect(url_for('journey', jid=journey.id))

            # confirm added stage
            flash('Successfully added new run.')
            return redirect(url_for('journey', jid=journey.id))
        else:
            return render_template('journeys_add_stage.html', journey=journey, form=form), 400
    return render_template('journeys_add_stage.html', journey=journey, form=form)
