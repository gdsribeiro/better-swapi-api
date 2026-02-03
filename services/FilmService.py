from models.Film import Film
from clients.SWAPIClient import SWAPIClient
import re

from concurrent.futures import ThreadPoolExecutor

class FilmService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_films(self, filters):
		tasks = {}

		# TODO Executar condicionalmente
    
		with ThreadPoolExecutor(max_workers=6) as executor:
			# Dispara a busca principal de personagens
			tasks['films'] = executor.submit(self.swapi.get_films)
			tasks['planets'] = executor.submit(self.swapi.get_data, "planets")
			tasks['species'] = executor.submit(self.swapi.get_data, "species")
			tasks['vehicles'] = executor.submit(self.swapi.get_data, "vehicles")
			tasks['characters'] = executor.submit(self.swapi.get_data, "people")
			tasks['starships'] = executor.submit(self.swapi.get_data, "starships")
		
		characters_names	= parse_to_set(tasks['characters'].result(), field="name")
		planets_names		= parse_to_set(tasks['planets'].result(), field="name")
		species_names		= parse_to_set(tasks['species'].result(), field="name")
		vehicles_names		= parse_to_set(tasks['vehicles'].result(), field="name")
		starships_names		= parse_to_set(tasks['starships'].result(), field="name")

		films = [
			Film(
				url = f.url,
				title = f.title,
				director = f.director,
				producer = f.producer,
				episode_id = f.episode_id,
				opening_crawl = f.opening_crawl,
				characters = [characters_names[url] for url in f.characters],
				species = [species_names[url] for url in f.species],
				starships = [starships_names[url] for url in f.starships],
				vehicles = [vehicles_names[url] for url in f.vehicles],
				planets = [planets_names[url] for url in f.planets],
				release_date = f.release_date
			)
			for f in tasks['films'].result()
		]
		
		films.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		# TODO Map

		# TODO Filter

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return films[start:end]
	
def parse_birth_year(birth_year):
	if birth_year:
		match = re.search(r"([\d\.]+)\s*(BBY|ABY)", birth_year, re.IGNORECASE)
		if match:
			year = float(match.group(1))
			period = match.group(2).upper()
			return year, period
	
	return 0, "Unknown"

def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}