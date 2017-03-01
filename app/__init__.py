import os

from flask import Flask


def create_app(config_obj):
    app = Flask(__name__)

    # initialize configs
    app.config.from_object(config_obj)

    # initialize extensions
    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

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
