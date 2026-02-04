from pydantic import BaseModel, Field
from typing import Literal, List
from DTOs.QueryParamsDTO import QueryParamsDTO

class PlanetsQueryParamsDTO(QueryParamsDTO) :
    url: str = ""
    climate: str = ""
    diameter: str = ""
    gravity: str = ""
    name: str = ""
    orbital_period: str = ""
    population: str = ""
    rotation_period: str = ""
    surface_water: str = ""
    terrain: str = ""
    residents: str = ""
    films: str = ""