from datetime import datetime
from typing import List

from pydantic import BaseModel


class AplicationCreate(BaseModel):
    user_name: str
    description: str


class AplicationRead(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime


class PaginatedAplications(BaseModel):
    items: List[AplicationRead]
    page: int
    size: int
