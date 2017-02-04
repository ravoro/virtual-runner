from flask import Blueprint, current_app

bp = Blueprint("template_filters", __name__)


@bp.app_template_filter()
def asset_release_version(url):
    version = current_app.config['RELEASE_VERSION']
    if version:
        url = "{}?v={}".format(url, version)
    return url
