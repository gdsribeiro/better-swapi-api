from pydantic import BaseModel, Field
from typing import Literal, List
from DTOs.QueryParamsDTO import QueryParamsDTO

class FilmsQueryParamsDTO(QueryParamsDTO) :
	title: str = ""
	director: str = ""
	producer: str = ""
	episode_id: int = 0
	opening_crawl: str = ""
	characters: str = ""
	species: str = ""
	starships: str = ""
	vehicles: str = ""
	planets: str = ""
	release_date: str = ""