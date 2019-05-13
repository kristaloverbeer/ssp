from typing import Optional

from flask import make_response, jsonify, Blueprint, request
from flask_cors import CORS

from src.database.schemas.visit_schema import VisitSchema
from src.logging.mixin import LoggingMixin
from src.repository.visit_repository import VisitRepository

logger = LoggingMixin().logger

visit_blueprint = Blueprint('visit_blueprint', __name__, url_prefix='/v1/visit')
CORS(visit_blueprint)

visit_schema = VisitSchema()
visits_repository = VisitRepository(visit_schema)


@visit_blueprint.route('/', methods=['GET'], defaults={'visit_id': None})
@visit_blueprint.route('/<int:visit_id>', methods=['GET'])
def visits(visit_id: Optional[str] = None):
    queried_visits, status = visits_repository.get(visit_id)
    return make_response(jsonify(queried_visits), status)


@visit_blueprint.route('/', methods=['POST'])
def create_visits():
    visits_to_add = request.get_json()
    logger.debug('Received {} records to insert'.format(len(visits_to_add)))

    message, status = visits_repository.insert(visits_to_add)
    return make_response(jsonify(message), status)
