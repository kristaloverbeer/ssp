from typing import Optional

from flask import make_response, jsonify, Blueprint, request
from flask_cors import CORS

from src.database.schemas.person_schema import PersonSchema
from src.logging.mixin import LoggingMixin
from src.repository.person_repository import PersonRepository

logger = LoggingMixin().logger

person_blueprint = Blueprint('person_blueprint', __name__, url_prefix='/v1/person')
CORS(person_blueprint)

person_schema = PersonSchema()
persons_repository = PersonRepository(person_schema)


@person_blueprint.route('/', methods=['GET'], defaults={'person_id': None})
@person_blueprint.route('/<int:person_id>', methods=['GET'])
def persons(person_id: Optional[str] = None):
    queried_persons, status = persons_repository.get(person_id)
    return make_response(jsonify(queried_persons), status)


@person_blueprint.route('/', methods=['POST'])
def create_persons():
    persons_to_add = request.get_json()
    logger.debug('Received {} records to insert'.format(len(persons_to_add)))

    message, status = persons_repository.insert(persons_to_add)
    return make_response(jsonify(message), status)
