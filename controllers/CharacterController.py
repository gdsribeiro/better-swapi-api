from DTOs.QueryParamsDTO import QueryParamsDTO
from services.CharacterService import CharacterService

class CharacterController:
	def get_personagens(query_params, payload):
		character_service = CharacterService()

		params = dict(query_params)
		filters = QueryParamsDTO.model_validate(params)

		characters = [c.model_dump() for c in character_service.get_characters(filters)]

		return characters