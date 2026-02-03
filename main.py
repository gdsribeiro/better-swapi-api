import functions_framework
from controllers.CharacterController import CharacterController
import json

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    path = request.path
    query_params = request.args
    request_json = request.get_json(silent=True)

    if path == '/personagens':
        return CharacterController.get_personagens(query_params, request_json)
