import os
from flask import Flask
from flask_flatpages import FlatPages
from frozen_flask import Frozen
from flask_bootstrap import Bootstrap
from config import config
from collections.abc import Mapping

pages = FlatPages()
freezer = Freezer()
bootstrap = Bootstrap()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    freezer.init_app(app)
    pages.init_app(app)
    bootstrap.init_app(app)

    #register blueprints:
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app