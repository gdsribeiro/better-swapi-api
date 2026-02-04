from models.Planet import Planet
from DTOs.QueryParamsDTO import QueryParamsDTO
from clients.SWAPIClient import SWAPIClient

from concurrent.futures import ThreadPoolExecutor

class PlanetService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_planets(self, filters):
		tasks = {}

		queries = {
			k: v
			for k, v in filters.model_dump(
				exclude_none=True,
				exclude=set(QueryParamsDTO.model_fields.keys())
			).items()
			if v != ""
		}

		fields = filters.fields.replace(" ", "").split(",") if filters.fields else None

		field_map = {
			"resident": ("people", "name", "residents"),
			"film": ("films", "title", "films")
		}

		with ThreadPoolExecutor(max_workers=6) as executor:
			tasks['planets'] = executor.submit(self.swapi.get_planets)
			
			for k, v in field_map.items():
				context, _, atribute = v
				filter_aux = getattr(filters, atribute).split(",")
				if (not fields or atribute in fields) and len(filter_aux):
					tasks[context] = executor.submit(self.swapi.get_data, context)

		results = {}
		for k, v in field_map.items():
			context, field, atribute = v
			filter_aux = getattr(filters, atribute).split(",")
			if (not fields or atribute in fields) and len(filter_aux):
				results[context] = parse_to_set(tasks[context].result(), field=field)

		planets = [
			Planet(
				url = p.url,
				name = p.name,
				climate = p.climate,
				diameter = p.diameter,
				gravity = p.gravity,
				orbital_period = p.orbital_period,
				population = p.population,
				rotation_period = p.rotation_period,
				surface_water = p.surface_water,
				terrain = p.terrain,
				residents = [results['people'][url] for url in p.residents] if (not fields or "residents" in fields) else [],
				films = [results['films'][url] for url in p.films] if (not fields or "films" in fields) else []
			)
			for p in tasks['planets'].result()
		]
		
		planets.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		filtered_planets = [
			p for p in planets 
			if all(
				value.lower() in str(getattr(p, key)).lower() 
				for key, value in queries.items()
			)
		]

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return [p.model_dump(include=set(fields) if fields else None) for p in filtered_planets[start:end]]

def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}