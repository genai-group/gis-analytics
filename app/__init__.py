from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    api.init_app(app)

    # Import and register your blueprints and resources here
    # from .api.routes import api_blueprint
    # app.register_blueprint(api_blueprint)

    return app