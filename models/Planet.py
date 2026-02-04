from pydantic import BaseModel
from typing import List
from datetime import datetime

class Planet(BaseModel):
    url: str
    climate: str
    diameter: str
    gravity: str
    name: str
    orbital_period: str
    population: str
    rotation_period: str
    surface_water: str
    terrain: str
    residents: List[str]
    films: List[str]