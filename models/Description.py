from pydantic import BaseModel
from typing import List
from datetime import datetime

class Description(BaseModel):
	title: str
	director: str
	producer: str
	episode_id: int
	description: str
	release_date: datetime