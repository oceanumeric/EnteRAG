import numpy as np
import pandas as pd
from tqdm import tqdm
from loguru import logger
from elasticsearch import Elasticsearch


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


def index_books():
    # for the demo, we will not set up secure connection
    client = Elasticsearch("http://localhost:9200")
    logger.info(f"Your Elasticsearch client is: {client.info()}")
    # construct the index
    client.indices.delete(index="goodreads_index", ignore_unavailable=True)

    # setup mappings
    mappings = {
        "properties": {
            "title": {"type": "text"},
            "authors": {"type": "text"},
            "link": {"type": "text"},
            "description": {"type": "text"},
            "average_rating": {"type": "float"},
            # we are using different names for text_review_counts
            "reviews_count": {"type": "integer"},
            "embeddings": {
                "type": "dense_vector",
                "dims": 768,
                "index": "true",
                "similarity": "cosine",
            },
        }
    }

    # create the index
    client.indices.create(index="goodreads_index", mappings=mappings)

    # read the data
    books = pd.read_csv("books_embeddings.csv")
    
    # convert the embeddings to numpy array
    books['embeddings'] = books['embeddings'].apply(lambda x: np.fromstring(x[1:-1], sep=','))
    

    operations = []
    # index the data
    for i, row in books.iterrows():
        operations.append({"index": {"_index": "goodreads_index"}})
        book = {
            "title": row["title"],
            "authors": row["authors"],
            "link": row["link"],
            "description": row["description"],
            "average_rating": row["average_rating"],
            "reviews_count": row["text_reviews_count"],
            "embeddings": row["embeddings"],
        }

        operations.append(book)
        
    print(len(operations))

    # we will add 1000 books at a time
    batch_size = 1000
    n_batches = len(operations) // batch_size
    bulk_batches = [
        operations[i * batch_size : (i + 1) * batch_size] for i in range(n_batches)
    ]

    for i, batch in enumerate(tqdm(bulk_batches)):
        client.bulk(index="goodreads_index", operations=batch, refresh=True)

    logger.success(f"Indexed {len(books)} books successfully")

    # run the first query
    response = client.search(
        index="goodreads_index", query={"match": {"title": {"query": "Blood"}}}
    )
    
    pretty_response(response)


if __name__ == "__main__":
    index_books()
