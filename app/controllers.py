from flask import flash
from flask import url_for, redirect, render_template

from app import app, db
from .forms import JourneysAddForm
from .models import Journey


@app.route('/')
def home():
    return redirect(url_for('journeys'))


@app.route('/journeys/<int:jid>')
def journey(jid):
    journey = Journey.query.get(jid)
    return render_template('journey.html', journey=journey)


@app.route('/journeys')
def journeys():
    journeys = Journey.query.all()
    return render_template('journeys.html', journeys=journeys)


@app.route('/journeys/add', methods=['GET', 'POST'])
def journeys_add():
    form = JourneysAddForm()
    if form.validate_on_submit():
        journey = Journey(
            str(form.name.data),
            float(form.start_lat.data),
            float(form.start_lng.data),
            float(form.finish_lat.data),
            float(form.finish_lng.data)
        )
        db.session.add(journey)
        db.session.commit()

        flash('Successfully created new journey.')
        return redirect(url_for('journey', jid=journey.id))
    return render_template('journeys_add.html', form=form)
