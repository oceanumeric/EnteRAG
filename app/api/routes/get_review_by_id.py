import json
from loguru import logger
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from models.get import GetReviewByIdResponse

from elasticsearch import Elasticsearch


router = APIRouter()


@router.get(
    "/get_review_by_id/{document_id}",
    response_model=GetReviewByIdResponse,
    name="get:book-review",
)
async def get_review_by_id(document_id: str):
    """Get a book review by id from elasticsearch

    Args:
        document_id (str): A document id

    Returns:
        GetReviewByIdResponse: A response model
    """
    client = Elasticsearch("http://localhost:9200/")
    response = client.get(index="goodreads_index", id=document_id)
    return GetReviewByIdResponse(reviews=response["_source"]["reviews"])
