from flask import flash
from flask import url_for, redirect, render_template

from app import app
from .forms import JourneysAddForm
from .models import mockDB, Journey, Coord


@app.route('/')
def home():
    return redirect(url_for('journeys'))


@app.route('/journeys/<int:jid>')
def journey(jid):
    return render_template('journey.html', journey=mockDB.get(jid))


@app.route('/journeys')
def journeys():
    return render_template('journeys.html', journeys=mockDB.values())


@app.route('/journeys/add', methods=['GET', 'POST'])
def journeys_add():
    form = JourneysAddForm()
    if form.validate_on_submit():
        id = max(mockDB.keys()) + 1
        mockDB[id] = Journey(
            id,
            str(form.name.data),
            Coord(float(form.start_lat.data), float(form.start_lng.data)),
            Coord(float(form.finish_lat.data), float(form.finish_lng.data)),
            []
        )
        flash('Successfully created new journey.')
        return redirect(url_for('journey', jid=id))
    return render_template('journeys_add.html', form=form)
