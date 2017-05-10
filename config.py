import os


class ProdConfig:
    BASE_DIR = os.path.dirname(__file__)
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mr|6I0fWE~!)yd]FwWKO7$j`.>D}Z,7OLOOlzV/xme<&S/f+xGDa|.Z=</Z2A[P|'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCWMRABwAqpwvWXw275HljKmIRMOvJ66Cg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SITE_VIRTUALRUNNER_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CUSTOM_TEMPLATES_DIR = os.path.join(BASE_DIR, 'app_data', 'templates')
    RELEASE_VERSION = 20170512


class DevConfig(ProdConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://virtualrunner:J6SqvOxROEYPokWA@localhost/virtualrunner'
    CUSTOM_TEMPLATES_DIR = None
    # DEBUG_TB_ENABLED = True
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    # DEBUG_TB_PROFILER_ENABLED = False
    # TEMPLATES_AUTO_RELOAD = True


class TestConfig(DevConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
