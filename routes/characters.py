from flask import Blueprint, request
from controllers.CharacterController import CharacterController

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/personagens', methods=['GET'])
def get_characters():
    return CharacterController.get_characters(request.args)