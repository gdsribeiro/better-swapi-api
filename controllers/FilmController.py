from DTOs.FilmsQueryParamsDTO import FilmsQueryParamsDTO
from services.FilmService import FilmService

class FilmController:
	def get_films(query_params):
		film_service = FilmService()

		params = dict(query_params)

		try:
			filters = FilmsQueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass

		films = film_service.get_films(filters)

		return films