from DTOs.StarshipsQueryParamsDTO import StarshipsQueryParamsDTO
from services.StarshipService import StarshipService

class StarshipController:
	def get_starships(query_params):
		starship_service = StarshipService()

		params = dict(query_params)

		try:
			filters = StarshipsQueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass
		starships = starship_service.get_starships(filters)

		return starships