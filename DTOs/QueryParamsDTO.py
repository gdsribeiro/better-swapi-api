from pydantic import BaseModel, Field
from typing import Literal, List

class QueryParamsDTO(BaseModel):
	page: int = Field(default=1, ge=1) 
	limit: int = Field(default=10, le=100)
	order: Literal['asc', 'desc'] = 'asc'
	sort_by: str = 'url'
	fields: str = ""