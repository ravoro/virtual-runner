import re
from flask import abort, flash, Blueprint, url_for, redirect, render_template, make_response
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.wrappers import Response

from .auth import anonymous_required
from .forms import JourneysAddForm, JourneyAddStageForm, UserLoginForm, UserRegisterForm
from .models import Journey, Stage, User
from .repositories import JourneyRepo, StageRepo, UserRepo

bp = Blueprint('controllers', __name__)


@bp.route('/')
@anonymous_required
def home() -> Response:
    return render_template('home.html')


@bp.route('/journeys')
@login_required
def journeys() -> Response:
    journeys = JourneyRepo.all_ordered(current_user.id)
    stats = {
        'total_distance': StageRepo.total_distance(current_user.id)
    }
    return render_template('journeys.html', journeys=journeys, stats=stats)


@bp.route('/journeys/add', methods=['GET', 'POST'])
@login_required
def journeys_add() -> Response:
    form = JourneysAddForm()
    if not form.is_submitted():
        return render_template('journeys_add.html', form=form)
    if not form.validate():
        return make_response(render_template('journeys_add.html', form=form), 400)

    journey = JourneyRepo.add(Journey(
        user_id=int(current_user.id),
        name=str(form.name.data),
        distance_meters=int(form.distance_meters.data),
        start_lat=float(form.start_lat.data),
        start_lng=float(form.start_lng.data),
        finish_lat=float(form.finish_lat.data),
        finish_lng=float(form.finish_lng.data),
    ))

    flash('Successfully created new journey.')
    return redirect(url_for('controllers.journey_details', jid=journey.id))


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
def journey_add_stage(jid: int) -> Response:
    journey = _get_journey_data(jid)
    if journey.is_completed:
        flash('The journey has been completed.')
        return redirect(url_for('controllers.journey_details', jid=journey.id))

    form = JourneyAddStageForm()
    if not form.is_submitted():
        return render_template('journey_add_stage.html', journey=journey, form=form)
    if not form.validate():
        return make_response(render_template('journey_add_stage.html', journey=journey, form=form), 400)

    StageRepo.add(Stage(
        journeys=journey,
        distance_meters=int(form.distance_meters.data)
    ))

    if journey.is_completed:
        flash(render_template('flash_messages/journey_add_stage_complete.html'), 'html')
    else:
        flash('Successfully added new run.')
    return redirect(url_for('controllers.journey_panorama', jid=journey.id))


def _get_journey_data(journey_id: int) -> Journey:
    """Fetch journey record owned by the user, including any relevant additional details. Raise 404 if not found."""
    journey = JourneyRepo.get(user_id=current_user.id, journey_id=journey_id)
    if not journey:
        return abort(404)
    stages = StageRepo.all_ordered(journey_id)
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

    is_email = re.match(r'\S+@\S+\.\S+', form.email_or_username.data)

    user = UserRepo.add(User(
        email=form.email_or_username.data if is_email else None,
        username=form.email_or_username.data if not is_email else None,
        password=form.password.data
    ))

    login_user(user)

    flash('Successfully registered.')
    return redirect(url_for('controllers.journeys'))


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

    flash('Successfully logged in.')
    return redirect(url_for('controllers.journeys'))


@bp.route('/logout', methods=['GET'])
@login_required
def user_logout() -> Response:
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('controllers.home'))
