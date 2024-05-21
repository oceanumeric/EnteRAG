from elasticsearch import Elasticsearch
from ml.model.embedding_generator import ONNXEmbeddingGenerator

def test_connection():
    generator = ONNXEmbeddingGenerator()
    query = "A romantic book for young adults"
    embeddings = generator.generate_embeddings(query)
    client = Elasticsearch("http://localhost:9200")

    response = client.search(
        index="goodreads_index",
        size=5,
        query={"match": {"title": {"query": "The Return of the King"}}},
    )

    assert response["hits"]["total"]["value"] > 0
    
    # test embedding search
    response = client.search(
        index="goodreads_index",
        knn = {
            "field": "embeddings",
            "query_vector": embeddings[0].tolist(),
            "k": 5,
            "num_candidates": 30
        }
    )
    
    assert response["hits"]["total"]["value"] > 0


def test_index_and_get():
    generator = ONNXEmbeddingGenerator()
    client = Elasticsearch("http://localhost:9200")
    review_text = "This is a test review from the test case"
    # test indexing
    book_review = {
        "title": "The Return of the King",
        "authors": "J.R.R. Tolkien",
        "description": "The inspiration for the upcoming original series on Prime Video, The Lord of the Rings: The Rings of Power.",
        "link": "https://www.goodreads.com/book/show/61215384-the-return-of-the-king",
        "average_rating": 4.56,
        "reviews_count": 0,
        "reviews": review_text,
        "embeddings":  generator.generate_embeddings(review_text)[0].tolist()
    }
    
    resp = client.index(index="goodreads_index", document=book_review)
    document_id = resp["_id"]
    
    # get the indexed document
    response = client.get(index="goodreads_index", id=document_id)
    assert response["_source"]["reviews"] == review_text