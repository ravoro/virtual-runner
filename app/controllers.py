from flask import abort, flash, Blueprint, url_for, redirect, render_template, make_response
from flask_login import login_user, login_required
from werkzeug.wrappers import Response

from .auth import anonymous_required
from .forms import JourneysAddForm, JourneysAddStageForm, UserLoginForm, UserRegisterForm
from .models import Journey, Stage, User
from .repositories import JourneyRepo, StageRepo, UserRepo

bp = Blueprint('controllers', __name__)


@bp.route('/')
@login_required
def home() -> Response:
    return redirect(url_for('controllers.journeys'))


@bp.route('/journeys')
@login_required
def journeys() -> Response:
    journeys = JourneyRepo.all_ordered()
    stats = {
        'total_distance': StageRepo.total_distance()
    }
    return render_template('journeys.html', journeys=journeys, stats=stats)


@bp.route('/journeys/add', methods=['GET', 'POST'])
@login_required
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
@login_required
def journey_details(jid: int) -> Response:
    journey = _get_journey_data(jid)
    return render_template('journey_details.html', journey=journey)


@bp.route('/journeys/<int:jid>/panorama')
@login_required
def journey_panorama(jid: int) -> Response:
    journey = _get_journey_data(jid)
    return render_template('journey_panorama.html', journey=journey)


@bp.route('/journeys/<int:jid>/add-run', methods=['GET', 'POST'])
@login_required
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


@bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
def user_register() -> Response:
    form = UserRegisterForm()
    if not form.is_submitted():
        return render_template('user_register.html', form=form)
    if not form.validate():
        return make_response(render_template('user_register.html', form=form), 400)

    UserRepo.add(User(
        email=form.email.data,
        password=form.password.data
    ))

    flash('Successfully registered.')
    return redirect(url_for('controllers.user_login'))


@bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def user_login() -> Response:
    form = UserLoginForm()
    if not form.is_submitted():
        return render_template('user_login.html', form=form)
    if not form.validate():
        return make_response(render_template('user_login.html', form=form), 400)

    user = UserRepo.get_by_email_or_username(form.email_or_username.data)
    login_user(user)

    flash('Successfully logged-in.')
    return redirect(url_for('controllers.journeys'))
