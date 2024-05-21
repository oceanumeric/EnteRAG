from elasticsearch import Elasticsearch
from ml.model.embedding_generator import ONNXEmbeddingGenerator

def pretty_response(response):
    if len(response["hits"]["hits"]) == 0:
        print("Your search returned no results.")
    else:
        for hit in response["hits"]["hits"]:
            id = hit["_id"]
            score = hit["_score"]
            title = hit["_source"]["title"]
            author = hit["_source"]["authors"]
            description = hit["_source"]["description"]
            link = hit["_source"]["link"]
            reviews_count = hit["_source"]["reviews_count"]
            pretty_output = f"\nID: {id}\nTitle: {title}\nAuthor: {author}\nDescription: {description}\nLink: {link}\nScore: {score}\n Reviews Count: {reviews_count}\n"
            print(pretty_output)
            
            
            
def test_elastic_search():
    generator = ONNXEmbeddingGenerator()
    query = "A romantic book for young adults"
    embeddings = generator.generate_embeddings(query)
    client = Elasticsearch("http://localhost:9200")

    response = client.search(
        index="goodreads_index",
        size=5,
        query={"match": {"title": {"query": "Harry Potter"}}},
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