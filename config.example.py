import os


class BaseConfig:
    SECRET_KEY = os.environ.get('VIRTUALRUNNER_SECRET_KEY')

    # Base directory for the project
    BASE_DIR = os.path.dirname(__file__)

    # Google Maps API key
    GOOGLE_MAPS_API_KEY = os.environ.get('VIRTUALRUNNER_GOOGLE_MAPS_API_KEY')

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('VIRTUALRUNNER_DATABASE_URI')

    # Directory storing custom templates for overriding default templates
    CUSTOM_TEMPLATES_DIR = os.path.join(BASE_DIR, 'app_data', 'templates')

    # Value used for distinguishing newer version of assets to keep browsers from using older cached versions
    # The value is added to the end of the asset URL. Ex: .../main.css?v=146
    RELEASE_VERSION = None


class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
