from DTOs.StarshipsQueryParamsDTO import StarshipsQueryParamsDTO
from services.StarshipService import StarshipService
from pydantic import ValidationError

class StarshipController:
	def get_starships(query_params):
		starship_service = StarshipService()

		params = dict(query_params)

		try:
			filters = StarshipsQueryParamsDTO.model_validate(params)
		except ValidationError as e:
			return {"error": "Validation Error", "details": e.errors()}, 400
		
		try:
			starships = starship_service.get_starships(filters)
		except Exception as e:
			return {"error": "Internal Server Error", "details": str(e)}, 500

		return starships