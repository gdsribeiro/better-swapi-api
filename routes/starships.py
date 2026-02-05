from flask import Blueprint, request
from controllers.StarshipController import StarshipController

starships_bp = Blueprint('starships', __name__)

@starships_bp.route('/naves', methods=['GET'])
def get_starships():
    return StarshipController.get_starships(request.args)