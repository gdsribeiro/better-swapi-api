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

		fields = filters.fields.replace(" ", "").split(",") if filters.fields else None

		print(fields)

		field_map = {
			"homeworld": ("planets", "name", "homeworld"),
			"specie": ("species", "name", "species"),
			"vehicle": ("vehicles", "name", "vehicles"),
			"film": ("films", "title", "films"),
			"starship": ("starships", "name", "starships"),
		}

		with ThreadPoolExecutor(max_workers=6) as executor:
			tasks['people'] = executor.submit(self.swapi.get_people)
			
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

		characters = [
			Character(
				url = p.url,
				name = p.name,
				birth_year = (parse := parse_birth_year(p.birth_year))[0],
				period = parse[1],
				homeworld = results['planets'][p.homeworld] if (not fields or "homeworld" in fields) else "",
				height = p.height,
				mass = p.mass,
				gender = p.gender,
				eye_color = p.eye_color.capitalize(),
				hair_color = p.hair_color.capitalize(),
				skin_color = p.skin_color.capitalize(),
				species = [results['species'][url] for url in p.species] if (not fields or "species" in fields) else [],
				vehicles = [results['vehicles'][url] for url in p.vehicles] if (not fields or "vehicles" in fields) else [],
				starships = [results['starships'][url] for url in p.starships] if (not fields or "starships" in fields) else [],
				films = [results['films'][url] for url in p.films] if (not fields or "films" in fields) else []
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

		return [c.model_dump(include=set(fields) if fields else None) for c in filtered_characters[start:end]]
	
def parse_birth_year(birth_year):
	if birth_year and (match := re.search(r"([\d\.]+)\s*(BBY|ABY)", birth_year, re.IGNORECASE)):
		year = float(match.group(1))
		period = match.group(2).upper()
		return year, period
	
	return 0, "Unknown"

def parse_to_set(result, field="name", id="url"):
	return {r.get(id): r.get(field) for r in result}