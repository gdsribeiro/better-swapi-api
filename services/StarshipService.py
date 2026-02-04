from models.Starship import Starship
from DTOs.QueryParamsDTO import QueryParamsDTO
from clients.SWAPIClient import SWAPIClient

from concurrent.futures import ThreadPoolExecutor

class StarshipService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_starships(self, filters):
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
			"pilot": ("people", "name", "pilots"),
			"film": ("films", "title", "films")
		}

		with ThreadPoolExecutor(max_workers=6) as executor:
			tasks['starships'] = executor.submit(self.swapi.get_starships)
			
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

		starships = [
			Starship(
				url = s.url,
				name = s.name,
				mglt = s.MGLT,
				cargo_capacity = s.cargo_capacity,
				consumables = s.consumables,
				cost_in_credits = s.cost_in_credits,
				crew = s.crew,
				hyperdrive_rating = s.hyperdrive_rating,
				length = s.length,
				manufacturer = s.manufacturer,
				max_atmosphering_speed = s.max_atmosphering_speed,
				model = s.model,
				passengers = s.passengers,
				starship_class = s.starship_class,
				pilots = [results['people'][url] for url in s.pilots] if (not fields or "pilots" in fields) else [],
				films = [results['films'][url] for url in s.films] if (not fields or "films" in fields) else []
			)
			for s in tasks['starships'].result()
		]
		
		starships.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		filtered_starships = [
			s for s in starships 
			if all(
				value.lower() in str(getattr(s, key)).lower() 
				for key, value in queries.items()
			)
		]

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return [s.model_dump(include=set(fields) if fields else None) for s in filtered_starships[start:end]]
	
def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}