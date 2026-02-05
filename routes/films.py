from flask import Blueprint, request
from controllers.FilmController import FilmController

films_bp = Blueprint('films', __name__)

@films_bp.route('/filmes', methods=['GET'])
def get_films():
    return FilmController.get_films(request.args)