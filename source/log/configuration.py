import os
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("EMIS_LOG_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_LOG_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "log-dev.sqlite")


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestingConfiguration(Configuration):

    SERVER_NAME = os.environ.get("EMIS_LOG_SERVER_NAME") or "localhost"
    TESTING = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_LOG_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "log-test.sqlite")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_LOG_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "log.sqlite")


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
