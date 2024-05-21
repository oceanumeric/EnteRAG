from typing import List
from pydantic import BaseModel


class Documents(BaseModel):
    title: str
    authors: str
    link: str
    average_rating: float
    reviews_count: int


class SemanticQueryResponse(BaseModel):
    documents: List[Documents]
