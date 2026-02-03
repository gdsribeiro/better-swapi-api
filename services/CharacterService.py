from models.Character import Character
from DTOs.QueryParamsDTO import QueryParamsDTO
from clients.SWAPIClient import SWAPIClient
import re

from concurrent.futures import ThreadPoolExecutor

class CharacterService:
	def __init__(self):
		self.swapi = SWAPIClient()

	def get_characters(self, filters):
		tasks = {}

		queries = {
			k: v
			for k, v in filters.model_dump(
				exclude_none=True,
				exclude=set(QueryParamsDTO.model_fields.keys())
			).items()
			if v != ""
		}
		print(queries)

		fields = filters.fields.replace(" ", "").split(",")

		homeworld = filters.homeworld.split(",")
		species = filters.species.split(",")
		vehicles = filters.vehicles.split(",")
		films = filters.films.split(",")
		starships = filters.starships.split(",")

		# TODO Pelo amor de deus refatora isso
    
		with ThreadPoolExecutor(max_workers=6) as executor:
			tasks['people'] = executor.submit(self.swapi.get_people)
			
			if "homeworld" in fields and len(homeworld):
				tasks['planets'] = executor.submit(self.swapi.get_data, "planets")
			
			if "species" in fields and len(species):
				tasks['species'] = executor.submit(self.swapi.get_data, "species")
			
			if "vehicles" in fields and len(vehicles):
				tasks['vehicles'] = executor.submit(self.swapi.get_data, "vehicles")
			
			if "films" in fields and len(films):
				tasks['films'] = executor.submit(self.swapi.get_data, "films")
			
			if "starships" in fields and len(starships):
				tasks['starships'] = executor.submit(self.swapi.get_data, "starships")
		
		if "homeworld" in fields and len(homeworld):
			planet_names = parse_to_set(tasks['planets'].result(), field="name")
			
		if "species" in fields and len(species):
			species_names = parse_to_set(tasks['species'].result(), field="name")
		
		if "vehicles" in fields and len(vehicles):
			vehicles_names = parse_to_set(tasks['vehicles'].result(), field="name")
		
		if"films" in fields and len(films):
			films_titles = parse_to_set(tasks['films'].result(), field="title")
		
		if "starships" in fields and len(starships):
			starships_names = parse_to_set(tasks['starships'].result(), field="name")

		characters = [
			Character(
				url = p.url,
				name = p.name,
				birth_year = (parse := parse_birth_year(p.birth_year))[0],
				period = parse[1],
				homeworld = planet_names[p.homeworld] if "homeworld" in fields else "",
				height = p.height,
				mass = p.mass,
				gender = p.gender,
				eye_color = p.eye_color.capitalize(),
				hair_color = p.hair_color.capitalize(),
				skin_color = p.skin_color.capitalize(),
				species = [species_names[url] for url in p.species] if "species" in fields else [],
				vehicles = [vehicles_names[url] for url in p.vehicles] if "vehicles" in fields else [],
				starships = [starships_names[url] for url in p.starships] if "starships" in fields else [],
				films = [films_titles[url] for url in p.films] if "films" in fields else []
			)
			for p in tasks['people'].result()
		]
		
		characters.sort(
			key=lambda c: getattr(c, filters.sort_by),
			reverse=filters.order=="desc"
		)

		filtered_characters = [
			c for c in characters 
			if all(
				value.lower() in str(getattr(c, key)).lower() 
				for key, value in queries.items()
			)
		]

		start = (filters.page - 1) * filters.limit
		end = start + filters.limit

		return [c.model_dump(include=set(fields)) for c in filtered_characters[start:end]]
	
def parse_birth_year(birth_year):
	if birth_year and (match := re.search(r"([\d\.]+)\s*(BBY|ABY)", birth_year, re.IGNORECASE)):
		year = float(match.group(1))
		period = match.group(2).upper()
		return year, period
	
	return 0, "Unknown"

def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}