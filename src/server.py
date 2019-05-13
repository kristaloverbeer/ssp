import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from src.api.index import index_blueprint
from src.api.ping import ping_blueprint
from src.api.v1.hotel import hotel_blueprint
from src.api.v1.person import person_blueprint
from src.api.v1.score import score_blueprint
from src.api.v1.visit import visit_blueprint
from src.configuration import Configuration
from src.database.models import db
from src.database.models.person import Person
from src.logging.mixin import LoggingMixin

logger = LoggingMixin().logger


def create_api(configuration: Configuration) -> Flask:
    logger.info('[SETUP] API Application')

    api = Flask(__name__)

    api.url_map.strict_slashes = False
    api.config['SQLALCHEMY_DATABASE_URI'] = configuration.database_uri
    api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api.config['SQLALCHEMY_ECHO'] = os.environ.get('SQLALCHEMY_ECHO', False)

    _register_blueprints(api)

    _initialize_admin_console(api)

    logger.info('[DONE] API Application')
    return api


def _register_blueprints(api_application: Flask) -> None:
    api_application.register_blueprint(ping_blueprint)
    api_application.register_blueprint(index_blueprint)
    api_application.register_blueprint(person_blueprint)
    api_application.register_blueprint(hotel_blueprint)
    api_application.register_blueprint(visit_blueprint)
    api_application.register_blueprint(score_blueprint)


def _initialize_admin_console(api_application: Flask) -> None:
    api_application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(api_application, name='Samu Social de Paris', template_mode='bootstrap3')

    admin.add_view(ModelView(Person, db.session))  # TODO: replace ModelView with a customized AdminView: https://danidee10.github.io/2016/11/14/flask-by-example-7.html


configuration = Configuration()
api = create_api(configuration)
db.init_app(api)
migration = Migrate(api, db)
