from DTOs.QueryParamsDTO import QueryParamsDTO
from services.FilmService import FilmService

class FilmController:
	def get_films(query_params):
		film_service = FilmService()

		params = dict(query_params)

		try:
			filters = QueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass

		films = film_service.get_films(filters)

		response = [c.model_dump() for c in films]

		return response