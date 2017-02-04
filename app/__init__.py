from flask import Flask


def create_app(config_obj):
    app = Flask(__name__)

    # initialize configs
    app.config.from_object(config_obj)

    # initialize extensions
    from .models import db
    db.init_app(app)

    # initialize blueprints
    from .controllers import bp as controllers
    app.register_blueprint(controllers)

    # initialize template filters
    from .templates.utils.filters import bp as template_filters
    app.register_blueprint(template_filters)

    return app
