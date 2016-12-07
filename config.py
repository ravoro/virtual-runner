class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mr|6I0fWE~!)yd]FwWKO7$j`.>D}Z,7OLOOlzV/xme<&S/f+xGDa|.Z=</Z2A[P|'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCWMRABwAqpwvWXw275HljKmIRMOvJ66Cg'


class ProdConfig(BaseConfig):
    pass


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
