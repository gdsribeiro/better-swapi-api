from DTOs.CharactersQueryParamsDTO import CharactersQueryParamsDTO
from services.CharacterService import CharacterService
from pydantic import ValidationError

class CharacterController:
	def get_characters(query_params):
		character_service = CharacterService()

		params = dict(query_params)
		
		try:
			filters = CharactersQueryParamsDTO.model_validate(params)
		except ValidationError as e:
			return {"error": "Validation Error", "details": e.errors()}, 400

		try:
			characters = character_service.get_characters(filters)
		except Exception as e:
			return {"error": "Internal Server Error", "details": str(e)}, 500

		return characters