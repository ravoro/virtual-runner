from flask import abort, flash, Blueprint, url_for, redirect, render_template, make_response
from werkzeug.wrappers import Response

from .forms import JourneysAddForm, JourneysAddStageForm
from .models import Journey, Stage
from .repositories import JourneyRepo, StageRepo

bp = Blueprint('controllers', __name__)


@bp.route('/')
def home() -> Response:
    return redirect(url_for('controllers.journeys'))


@bp.route('/journeys')
def journeys() -> Response:
    journeys = JourneyRepo.all_ordered()
    return render_template('journeys.html', journeys=journeys)


@bp.route('/journeys/add', methods=['GET', 'POST'])
def journeys_add() -> Response:
    form = JourneysAddForm()
    if form.is_submitted():
        if form.validate():
            journey = JourneyRepo.create(Journey(
                name=str(form.name.data),
                distance_meters=int(form.distance_meters.data),
                start_lat=float(form.start_lat.data),
                start_lng=float(form.start_lng.data),
                finish_lat=float(form.finish_lat.data),
                finish_lng=float(form.finish_lng.data),
            ))
            flash('Successfully created new journey.')
            return redirect(url_for('controllers.journey', jid=journey.id))
        else:
            return make_response(render_template('journeys_add.html', form=form), 400)
    else:
        return render_template('journeys_add.html', form=form)


@bp.route('/journeys/<int:jid>')
def journey(jid: int) -> Response:
    journey = JourneyRepo.get(jid)
    if not journey:
        return abort(404)
    stages = StageRepo.all_ordered(jid)

    completed_fraction = 1
    if journey.completed_distance < journey.distance_meters:
        completed_fraction = journey.completed_distance / journey.distance_meters
    journey.completed_fraction = completed_fraction

    return render_template('journey.html', journey=journey, stages=stages)


@bp.route('/journeys/<int:jid>/add-run', methods=['GET', 'POST'])
def journeys_add_stage(jid: int) -> Response:
    journey = JourneyRepo.get(jid)
    if not journey:
        return abort(404)

    if journey.is_completed:
        flash('The journey has been completed.')
        return redirect(url_for('controllers.journey', jid=journey.id))

    form = JourneysAddStageForm()
    if form.is_submitted():
        if form.validate():
            StageRepo.create(Stage(
                distance_meters=int(form.distance_meters.data),
                journey=journey
            ))

            message = 'Successfully added new run.'
            if journey.is_completed:
                message = """
                    <strong>Congratulations!</strong>
                    You\'ve completed the journey. Howay!
                    <br/><br/>
                    <iframe height="250px"
                            width="500px"
                            src="https://www.youtube.com/embed/G-5CwNAStbM?autoplay=1&showinfo=0&controls=0&modestbranding=1"
                            frameborder="0"
                            allowfullscreen></iframe>"""
            flash(message, 'html')
            return redirect(url_for('controllers.journey', jid=journey.id))
        else:
            return make_response(render_template('journeys_add_stage.html', journey=journey, form=form), 400)
    else:
        return render_template('journeys_add_stage.html', journey=journey, form=form)
