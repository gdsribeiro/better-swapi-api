import functions_framework
from controllers.CharacterController import CharacterController
from controllers.FilmController import FilmController
from controllers.PlanetController import PlanetController
from controllers.StarshipController import StarshipController

@functions_framework.http
def main_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """

    path = request.path
    query_params = request.args
    #request_json = request.get_json(silent=True)
    
    if path == '/filmes':
        return FilmController.get_films(query_params)

    if path == '/personagens':
        return CharacterController.get_characters(query_params)
    
    if path == '/planetas':
        return PlanetController.get_planets(query_params)
    
    if path == '/naves':
        return StarshipController.get_starships(query_params)

    return "Not Found", 404