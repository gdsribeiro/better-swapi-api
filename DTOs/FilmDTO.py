from pydantic import BaseModel
from typing import List
from datetime import datetime

class FilmDTO(BaseModel):
    url: str
    title: str
    director: str
    producer: str
	
    episode_id: int
    opening_crawl: str

    characters: List[str]
    species: List[str]
    starships: List[str]
    vehicles: List[str]
    planets: List[str]
	
    release_date: datetime 
    created: datetime
    edited: datetime