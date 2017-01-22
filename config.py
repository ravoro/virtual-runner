import os


class BaseConfig(object):
    BASE_DIR = os.path.dirname(__file__)
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mr|6I0fWE~!)yd]FwWKO7$j`.>D}Z,7OLOOlzV/xme<&S/f+xGDa|.Z=</Z2A[P|'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCWMRABwAqpwvWXw275HljKmIRMOvJ66Cg'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'journeys.db')
    RELEASE_VERSION = None


class ProdConfig(BaseConfig):
    RELEASE_VERSION = 20170119.3


class DevConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True


class TestConfig(BaseConfig):
    TESTING = True
