import json
from loguru import logger
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from models.semantic import SemanticQueryResponse

from elasticsearch import Elasticsearch
from ml.model.embedding_generator import ONNXEmbeddingGenerator


class Query(BaseModel):
    query: str
    
    
router = APIRouter()


def semantic_search(query: Query) -> List[dict]:
    """Search for similar documents based on the query

    Args:
        query (Query): A query object

    Returns:
        List[dict]: A list of documents
    """
    client = Elasticsearch("http://localhost:9200/")
    
    # embedding query
    generator = ONNXEmbeddingGenerator()
    embeddings = generator.generate_embeddings(query.query)
    
    # search for similar documents
    response = client.search(
        index = "goodreads_index",
        size = 5,
        query = {
            "multi_match": {
                "query": query.query,
                "fields": ["title", "authors", "description"]
            }
        },
        knn = {
            "field": "embeddings",
            "query_vector": embeddings[0].tolist(),
            "k": 5,
            "num_candidates": 20
        }
    )
    
    search_results = []
    
    for hit in response["hits"]["hits"]:
        temp_dict = {
            "title": hit["_source"]["title"],
            "authors": hit["_source"]["authors"],
            "link": hit["_source"]["link"],
            "average_rating": hit["_source"]["average_rating"],
            "reviews_count": hit["_source"]["reviews_count"]
        }
        
        search_results.append(temp_dict)
    
    # sort the search results by average rating and reviews count
    # search_results = sorted(search_results, key=lambda x: (x["reviews_count"], x["average_rating"]), reverse=True)
    
    return search_results


@router.post(
    "/semantic_query",
    response_model=SemanticQueryResponse,
    name="semantic:query",
)
async def semantic_query(query: Query):
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")
    
    results = semantic_search(query)
    
    return SemanticQueryResponse(documents=results)