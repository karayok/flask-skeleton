import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    # SQLAlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'stage': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
