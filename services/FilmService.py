from models.Film import Film
from DTOs.QueryParamsDTO import QueryParamsDTO
from clients.SWAPIClient import SWAPIClient

from concurrent.futures import ThreadPoolExecutor

class FilmService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_films(self, filters):
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
			"character": ("people", "name", "characters"),
			"planet": ("planets", "name", "planets"),
			"specie": ("species", "name", "species"),
			"vehicle": ("vehicles", "name", "vehicles"),
			"starship": ("starships", "name", "starships"),
		}
    
		with ThreadPoolExecutor(max_workers=6) as executor:
			tasks['films'] = executor.submit(self.swapi.get_films)

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

		films = [
			Film(
				url = f.url,
				title = f.title,
				director = f.director,
				producer = f.producer,
				episode_id = f.episode_id,
				opening_crawl = f.opening_crawl,
				characters = [results['people'][url] for url in f.characters] if (not fields or 'characters' in fields) else [],
				species = [results['species'][url] for url in f.species] if (not fields or "species" in fields) else [],
				starships = [results['starships'][url] for url in f.starships] if (not fields or 'starships' in fields) else [],
				vehicles = [results['vehicles'][url] for url in f.vehicles] if (not fields or 'vehicles' in fields) else [],
				planets = [results['planets'][url] for url in f.planets] if (not fields or 'planets' in fields) else [],
				release_date = f.release_date
			)
			for f in tasks['films'].result()
		]
		
		films.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		filtered_films = [
			f for f in films 
			if all(
				str(value).lower() in str(getattr(f, key)).lower() 
				for key, value in queries.items()
			)
		]

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return [f.model_dump(include=set(fields) if fields else None) for f in filtered_films[start:end]]

def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}