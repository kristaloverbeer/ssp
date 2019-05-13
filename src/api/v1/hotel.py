from typing import Optional

from flask import make_response, jsonify, Blueprint, request
from flask_cors import CORS

from src.database.schemas.hotel_schema import HotelSchema
from src.logging.mixin import LoggingMixin
from src.repository.hotel_repository import HotelRepository

logger = LoggingMixin().logger

hotel_blueprint = Blueprint('hotel_blueprint', __name__, url_prefix='/v1/hotel')
CORS(hotel_blueprint)

hotel_schema = HotelSchema()
hotels_repository = HotelRepository(hotel_schema)


@hotel_blueprint.route('/', methods=['POST'])
def create_hotel():
    hotel_to_add = request.get_json()

    logger.debug('Inserting hotel: {}'.format(hotel_to_add))

    message, status = hotels_repository.insert(hotel_to_add)
    return make_response(jsonify(message), status)


@hotel_blueprint.route('/', methods=['GET'], defaults={'hotel_id': None})
@hotel_blueprint.route('/<int:hotel_id>', methods=['GET'])
def hotels(hotel_id: Optional[int] = None):
    queried_hotels, status = hotels_repository.get(hotel_id)
    return make_response(jsonify(queried_hotels), status)


@hotel_blueprint.route('/', methods=['PUT', 'PATCH'], defaults={'hotel_id': None})
@hotel_blueprint.route('/<int:hotel_id>', methods=['PUT', 'PATCH'])
def update_hotels(hotel_id: Optional[str] = None):
    pass
