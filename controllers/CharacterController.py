from DTOs.CharactersQueryParamsDTO import CharactersQueryParamsDTO
from services.CharacterService import CharacterService

class CharacterController:
	def get_characters(query_params):
		character_service = CharacterService()

		params = dict(query_params)
		
		try:
			filters = CharactersQueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass
		characters = character_service.get_characters(filters)

		return characters