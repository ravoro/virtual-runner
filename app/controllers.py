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
    stats = {
        'total_distance': StageRepo.total_distance()
    }
    return render_template('journeys.html', journeys=journeys, stats=stats)


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
            return redirect(url_for('controllers.journey_details', jid=journey.id))
        else:
            return make_response(render_template('journeys_add.html', form=form), 400)
    else:
        return render_template('journeys_add.html', form=form)


@bp.route('/journeys/<int:jid>')
def journey_details(jid: int) -> Response:
    journey = _get_journey_data(jid)
    return render_template('journey_details.html', journey=journey)


@bp.route('/journeys/<int:jid>/panorama')
def journey_panorama(jid: int) -> Response:
    journey = _get_journey_data(jid)
    return render_template('journey_panorama.html', journey=journey)


@bp.route('/journeys/<int:jid>/add-run', methods=['GET', 'POST'])
def journeys_add_stage(jid: int) -> Response:
    journey = _get_journey_data(jid)

    if journey.is_completed:
        flash('The journey has been completed.')
        return redirect(url_for('controllers.journey_details', jid=journey.id))

    form = JourneysAddStageForm()
    if form.is_submitted():
        if form.validate():
            StageRepo.create(Stage(
                distance_meters=int(form.distance_meters.data),
                journey=journey
            ))

            if journey.is_completed:
                flash(render_template('flash_messages/journey_add_stage_complete.html'), 'html')
            else:
                flash('Successfully added new run.')
            return redirect(url_for('controllers.journey_panorama', jid=journey.id))
        else:
            return make_response(render_template('journey_add_stage.html', journey=journey, form=form), 400)
    else:
        return render_template('journey_add_stage.html', journey=journey, form=form)


def _get_journey_data(jid: int) -> Journey:
    """Fetch journey record including any relevant additional details. Raise 404 exception if journey not found."""
    journey = JourneyRepo.get(jid)
    if not journey:
        return abort(404)
    stages = StageRepo.all_ordered(jid)
    journey.stages_ordered = stages
    return journey
