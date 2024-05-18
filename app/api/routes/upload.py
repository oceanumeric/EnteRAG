import json

from typing import List
from pydantic import BaseModel, HttpUrl
from fastapi import APIRouter, HTTPException


from models.upload import UploadReviewResponse


# create bookreview class


class BookReview(BaseModel):
    title: str
    author: str
    description: str
    link: HttpUrl


router = APIRouter()


# function to index book review
def index_review(book_review: BookReview) -> str:
    """Index a book review to elasticsearch

    Args:
        book_review (BookReview): A book review object

    Returns:
        str: a document id returned from elasticsearch
    """
    return "this is your document id"


# create endpoint for uploading book review
@router.post(
    "/upload",
    response_model=UploadReviewResponse,
    name="upload:book-review",
)
async def upload_review(book_review: BookReview):
    if not book_review:
        raise HTTPException(status_code=404, detail="'book_review' argument invalid!")
    try:
        document_id = index_review(book_review)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Exception: {err}")

    return UploadReviewResponse(document_id=document_id)
