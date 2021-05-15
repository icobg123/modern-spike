import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # MONGO_HOST = os.environ['MONGO_HOST']
    # MONGO_PORT = os.environ['MONGO_PORT']
    # MONGO_DB = os.environ['MONGO_DB']
    # MONGO_USER = os.environ['MONGO_USER']
    # MONGO_PASS = os.environ['MONGO_PASS']

    MONGO_URI = os.environ['DB_URI']
    # MONGO_URI = "mongodb://" + MONGO_USER + ":" + MONGO_PASS + "@" + MONGO_HOST + ":" + MONGO_PORT + "/" + MONGO_DB
    # DB_URI = os.environ['DB_URI']
    # MONGO
    # print(MONGO_URI)
    # MONGO_NEW_URI =


    # MONGO_URI = os.environ['mlab_DB_URI']
    # MONGO_URI = os.environ['DB_URI']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
