from pydantic import BaseModel
from typing import List, Literal
from enum import Enum
from datetime import datetime
'''
class EyeColor(str, Enum):
	BLUE = "Blue"

class HairColor(str, Enum):
	BLOND = "Blond"

class SkinColor(str, Enum):
	FAIR = "Fair"
'''
class Character(BaseModel):
	url: str
	name: str
	birth_year: float
	period: str
	homeworld: str
	height: str
	mass: str
	gender: str
	eye_color: str
	hair_color: str
	skin_color: str

	species: List[str]
	vehicles: List[str]
	starships: List[str]
	films: List[str]