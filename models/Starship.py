from pydantic import BaseModel
from typing import List
from datetime import datetime

class Starship(BaseModel):
    url: str
    mglt: str
    cargo_capacity: str
    consumables: str
    cost_in_credits: str
    crew: str
    hyperdrive_rating: str
    length: str
    manufacturer: str
    max_atmosphering_speed: str
    model: str
    name: str
    passengers: str
    films: List[str]
    pilots: List[str]
    starship_class: str