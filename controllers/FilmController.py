from DTOs.FilmsQueryParamsDTO import FilmsQueryParamsDTO
from services.FilmService import FilmService
from pydantic import ValidationError

class FilmController:
	def get_films(query_params):
		film_service = FilmService()

		params = dict(query_params)

		try:
			filters = FilmsQueryParamsDTO.model_validate(params)
		except ValidationError as e:
			return {"error": "Validation Error", "details": e.errors()}, 400

		try:
			films = film_service.get_films(filters)
		except Exception as e:
			return {"error": "Internal Server Error", "details": str(e)}, 500

		return films
	
	def get_film_description(query_params):
		film_service = FilmService()

		params = dict(query_params)

		try:
			filters = FilmsQueryParamsDTO.model_validate(params)
		except ValidationError as e:
			return {"error": "Validation Error", "details": e.errors()}, 400

		try:
			description = film_service.get_film_description(filters)
		except Exception as e:
			return {"error": "Internal Server Error", "details": str(e)}, 500

		return description