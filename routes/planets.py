from flask import Blueprint, request
from controllers.PlanetController import PlanetController

planets_bp = Blueprint('planets', __name__)

@planets_bp.route('/planetas', methods=['GET'])
def get_planets():
    return PlanetController.get_planets(request.args)