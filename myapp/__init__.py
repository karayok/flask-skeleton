from flask import Flask

from myapp import config
from myapp.database import db, Database

__version__ = '0.1'
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    db.init_app(app)
    Database(app)
