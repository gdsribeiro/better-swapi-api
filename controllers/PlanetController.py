from DTOs.PlanetsQueryParamsDTO import PlanetsQueryParamsDTO
from services.PlanetService import PlanetService
from pydantic import ValidationError

class PlanetController:
	def get_planets(query_params):
		planet_service = PlanetService()

		params = dict(query_params)

		try:
			filters = PlanetsQueryParamsDTO.model_validate(params)
		except ValidationError as e:
			return {"error": "Validation Error", "details": e.errors()}, 400
		
		try:
			planets = planet_service.get_planets(filters)
		except Exception as e:
			return {"error": "Internal Server Error", "details": str(e)}, 500

		return planets