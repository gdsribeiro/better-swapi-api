from flask import Blueprint, request
from controllers.FilmController import FilmController

films_bp = Blueprint('films', __name__)

@films_bp.route('/filmes', methods=['GET'])
def get_films():
    return FilmController.get_films(request.args)

@films_bp.route('/filmes/descricao', methods=['GET'])
def get_films_description():
    return FilmController.get_film_description(request.args)