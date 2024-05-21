import pandas as pd
from tqdm import tqdm
from loguru import logger
from elasticsearch import Elasticsearch


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

    # we will add 1000 books at a time
    batch_size = 1000
    n_batches = len(operations) // batch_size
    bulk_batches = [
        operations[i * batch_size : (i + 1) * batch_size] for i in range(n_batches)
    ]

    for i, batch in enumerate(tqdm(bulk_batches)):
        client.bulk(index="goodreads_index", operations=batch, refresh=True)

    logger.success(f"Indexed {len(books)} books successfully")


if __name__ == "__main__":
    index_books()
