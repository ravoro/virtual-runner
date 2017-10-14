import sys

import jinja2
import os
from flask import Flask

if sys.version_info < (3, 5):
    print("Warning: code is written for Python3.5+. You may run into issues running a different version of python.")


def create_app(config_obj):
    app = Flask(__name__)

    # initialize configs
    app.config.from_object(config_obj)

    # initialize extensions
    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    from .auth import login_manager
    login_manager.init_app(app)

    # prioritize a custom template directory (if one is configured)
    if app.config.get('CUSTOM_TEMPLATES_DIR'):
        app.jinja_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader(app.config['CUSTOM_TEMPLATES_DIR']),
            app.jinja_loader
        ])

    # initialize blueprints
    from .controllers import bp as controllers
    app.register_blueprint(controllers)

    # initialize template filters
    from .templates.utils.filters import bp as template_filters
    app.register_blueprint(template_filters)

    return app


# create app from FLASK_CONFIG envvar, where FLASK_CONFIG is name of config object to use (ex: "config.DevConfig")
if os.environ.get('FLASK_CONFIG'):
    app_from_envvar = create_app(os.environ.get('FLASK_CONFIG'))
