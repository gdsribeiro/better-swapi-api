from pydantic import BaseModel
from typing import List
from datetime import datetime

class PeopleDTO(BaseModel):
    birth_year: str
    eye_color: str
    films: List[str]
    gender: str
    hair_color: str
    height: str
    homeworld: str
    mass: str
    name: str
    skin_color: str
    created: datetime
    edited: datetime
    species: List[str]
    starships: List[str]
    url: str
    vehicles: List[str]