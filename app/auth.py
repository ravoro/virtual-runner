from functools import wraps
from typing import Optional

from flask import flash, redirect, url_for
from flask_login import LoginManager, current_user

from .models import User
from .repositories import UserRepo

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    flash('Please log in to proceed.')
    return redirect(url_for('controllers.user_login'))


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return UserRepo.get(int(user_id))


def anonymous_required(f):
    """Decorator that requires anonymous users and redirects away from the page if the user is logged in."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('controllers.journeys'))
        return f(*args, **kwargs)

    return wrapper
