from datetime import datetime

from flask import Blueprint, current_app

bp = Blueprint("template_filters", __name__)


@bp.app_template_filter()
def asset_release_version(url):
    version = current_app.config['RELEASE_VERSION']
    if version:
        return "{}?v={}".format(url, version)
    return url


@bp.app_template_filter()
def format_date(val):
    if isinstance(val, datetime):
        return val.strftime('%d %B %Y')
    return val


@bp.app_template_filter()
def meters_to_km(val):
    if isinstance(val, int):
        return '{:.2g}'.format(float(val / 1000))
    return val
