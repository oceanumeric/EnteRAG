import json
from loguru import logger
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from models.upload import UploadReviewResponse



from elasticsearch import Elasticsearch
from ml.model.embedding_generator import ONNXEmbeddingGenerator


# create bookreview class
class BookReview(BaseModel):
    reviews: str
    

router = APIRouter()


# function to index book review
def index_review(book_review: BookReview) -> str:
    """Index a book review to elasticsearch

    Args:
        book_review (BookReview): A book review object

    Returns:
        str: a document id returned from elasticsearch
    """
    client = Elasticsearch("http://localhost:9200/")
    
    # embedding reviews
    generator = ONNXEmbeddingGenerator()
    embeddings = generator.generate_embeddings(book_review.reviews)
    book_review = {
        "title": "The Return of the King",
        "authors": "J.R.R. Tolkien",
        "description": "The inspiration for the upcoming original series on Prime Video, The Lord of the Rings: The Rings of Power.",
        "link": "https://www.goodreads.com/book/show/61215384-the-return-of-the-king",
        "average_rating": 4.56,
        "reviews_count": 0,
        "reviews": book_review.reviews,
        "embeddings":  embeddings[0].tolist()
    }
    resp = client.index(index="goodreads_index", document=book_review)
    
    document_id = resp["_id"]
    return document_id


# create endpoint for uploading book review
@router.post(
    "/upload_review",
    response_model=UploadReviewResponse,
    name="upload:book-review",
)
async def upload_review(book_review: BookReview):
    if not book_review:
        raise HTTPException(status_code=404, detail="'book_review' argument invalid!")
    try:
        document_id = index_review(book_review)
        logger.info(f"Document has been indexed with id: {document_id}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Exception: {err}")

    return UploadReviewResponse(document_id=document_id)
