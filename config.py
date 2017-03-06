import os


class ProdConfig:
    BASE_DIR = os.path.dirname(__file__)
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mr|6I0fWE~!)yd]FwWKO7$j`.>D}Z,7OLOOlzV/xme<&S/f+xGDa|.Z=</Z2A[P|'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCWMRABwAqpwvWXw275HljKmIRMOvJ66Cg'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'journeys.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RELEASE_VERSION = 20170306


class DevConfig(ProdConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ProdConfig.BASE_DIR, 'tmp', 'local.db')
    # DEBUG_TB_ENABLED = True
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    # DEBUG_TB_PROFILER_ENABLED = False
    # TEMPLATES_AUTO_RELOAD = True


class TestConfig(DevConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
