from flask import make_response, jsonify, Blueprint
from flask_cors import CORS

from src.logging.mixin import LoggingMixin

logger = LoggingMixin().logger

score_blueprint = Blueprint('score_blueprint', __name__, url_prefix='/v1/score')
CORS(score_blueprint)


@score_blueprint.route('/hotel', methods=['GET'])
def score_hotel():
    scored_hotel = [{'id': 1, 'score': 0.82}, {'id': 2, 'score': 0.18}]
    return make_response(jsonify(scored_hotel), 200)
