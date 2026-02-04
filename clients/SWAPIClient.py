import requests
from DTOs.PeopleDTO import PeopleDTO
from DTOs.FilmDTO import FilmDTO
from DTOs.StarshipDTO import StarshipDTO
from DTOs.PlanetDTO import PlanetDTO

class SWAPIClient:
	def __init__(self):
		self.base_url = "https://swapi.dev/api"

	def get_data(self, context):
		try:
			data_aux = []
			next = f"{self.base_url}/{context}"

			while True:
				print(f"Request in {context}")
				response = requests.get(next)
				response.raise_for_status()

				status = response.status_code
				if status == 200:
					result = response.json()
					data = result["results"]
					next = result["next"]
					if data:
						data_aux = data_aux + data

				if not next:
					break

			return data_aux

		except requests.HTTPError as e:
			if e.response.status_code == 404:
				print("Dado não encontrado na API.")
				return None
			print(f"Erro de API: {e}")
			raise

	def get_people(self):
		try:
			data = self.get_data("people")
			return [PeopleDTO.model_validate(r) for r in data]
		
		#except ValidationError as e:
		#	print(f"A API retornou dados inválidos! Contrato quebrado: {e}")
		#	raise ValueError("Erro de integração: Dados da API inválidos")
		
		finally:
			pass

	def get_films(self):
		try:
			data = self.get_data("films")
			return [FilmDTO.model_validate(r) for r in data]
		
		#except ValidationError as e:
		#	print(f"A API retornou dados inválidos! Contrato quebrado: {e}")
		#	raise ValueError("Erro de integração: Dados da API inválidos")
		
		finally:
			pass

	def get_starships(self):
		try:
			data = self.get_data("starships")
			return [StarshipDTO.model_validate(r) for r in data]
		
		#except ValidationError as e:
		#	print(f"A API retornou dados inválidos! Contrato quebrado: {e}")
		#	raise ValueError("Erro de integração: Dados da API inválidos")
		
		finally:
			pass

	

	def get_planets(self):
		try:
			data = self.get_data("planets")
			return [PlanetDTO.model_validate(r) for r in data]
		
		#except ValidationError as e:
		#	print(f"A API retornou dados inválidos! Contrato quebrado: {e}")
		#	raise ValueError("Erro de integração: Dados da API inválidos")
		
		finally:
			pass