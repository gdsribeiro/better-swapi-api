from DTOs.QueryParamsDTO import QueryParamsDTO
from services.CharacterService import CharacterService

class CharacterController:
	def get_characters(query_params):
		character_service = CharacterService()

		params = dict(query_params)
		
		try:
			filters = QueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass
		characters = character_service.get_characters(filters)

		response = [c.model_dump() for c in characters]

		return response