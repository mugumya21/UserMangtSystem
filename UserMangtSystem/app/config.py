class Config(object):
    DEBUG = False
    TESTING = False
    DB_NAME = 'production-db'
    DB_USERNAME = "root"
    DB_PASSWORD = "rreecedc"
    SECRET_KEY = "ffdfvfbgbfvarthn"



class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEVELOPMENT = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "foodoo"


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "testing-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "testppp"
   
