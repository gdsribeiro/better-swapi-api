from DTOs.PlanetsQueryParamsDTO import PlanetsQueryParamsDTO
from services.PlanetService import PlanetService

class PlanetController:
	def get_planets(query_params):
		planet_service = PlanetService()

		params = dict(query_params)

		try:
			filters = PlanetsQueryParamsDTO.model_validate(params)
		except:
			# TODO Tratar erro
			pass
		planets = planet_service.get_planets(filters)

		return planets