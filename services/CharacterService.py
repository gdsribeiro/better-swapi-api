from models.Character import Character
from clients.SWAPIClient import SWAPIClient
import re

from concurrent.futures import ThreadPoolExecutor

class CharacterService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_characters(self, filters):
		tasks = {}
    
		with ThreadPoolExecutor(max_workers=6) as executor:
			# Dispara a busca principal de personagens
			tasks['people'] = executor.submit(self.swapi.get_people)
			tasks['planets'] = executor.submit(self.swapi.get_data, "planets")
			tasks['species'] = executor.submit(self.swapi.get_data, "species")
			tasks['vehicles'] = executor.submit(self.swapi.get_data, "vehicles")
			tasks['films'] = executor.submit(self.swapi.get_data, "films")
			tasks['starships'] = executor.submit(self.swapi.get_data, "starships")
		
		people				= tasks['people'].result()
		planet_names		= parse_to_set(tasks['planets'].result(), field="name")
		species_names		= parse_to_set(tasks['species'].result(), field="name")
		vehicles_names		= parse_to_set(tasks['vehicles'].result(), field="name")
		starships_names		= parse_to_set(tasks['starships'].result(), field="name")
		films_names			= parse_to_set(tasks['films'].result(), field="title")

		characters = [
			Character(
				url = p.url,
				name = p.name,
				birth_year = (parse := parse_birth_year(p.birth_year))[0],
				period = parse[1],
				homeworld = planet_names[p.homeworld],
				height = p.height,
				mass = p.mass,
				gender = p.gender,
				eye_color = p.eye_color.capitalize(),
				hair_color = p.hair_color.capitalize(),
				skin_color = p.skin_color.capitalize(),
				species = [species_names[name] for name in p.species],
				vehicles = [vehicles_names[name] for name in p.vehicles],
				starships = [starships_names[name] for name in p.starships],
				films = [films_names[name] for name in p.films],
				created_at = p.created,
				last_edited = p.edited
			)
			for p in people
		]
		
		characters.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return characters[start:end]
	
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