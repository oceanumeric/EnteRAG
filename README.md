# AI-powered Enterprise RAG


<p align="center">
<img src="https://github.com/oceanumeric/EnteRAG/blob/master/app/static/images/enterag-logo.png?raw=true" width="200" height="200" />
</p>

This project is built for many interviews during my job hunting process, which could show:

- My **data engineering skills**, check [ETL.ipynb](notebooks/ETL.ipynb)
    - you need good data engineering skills to handle 1.5M records, meaning you can train the model, index the data, and search for books in a reasonable time
- My **machine learning skills**, check [sentence_embedding.ipynb](notebooks/sentence_embedding.ipynb) and [onnx_runtime.ipynb](notebooks/onnx_runtime.ipynb)
- My **software engineering skills in production envrionment**, check the project structure and code quality

This project is the implementation of an AI-powered Enterprise RAG (Retrieval-augmented generation). It uses a pre-trained model to generate embeddings for books and then uses Elasticsearch to index and search for books by using multi-modal search:

- traditional text search
- 🧮 consine similarity search using embeddings (meaning books are recommended based on not just key words but semantic, user preferences, etc. which are all embedded as a vector)
- I did not choose a vector database as elasticsearch provides vector storage and search capabilities. It is not as good as a vector database but it is good enough for this project. [Milvus](https://milvus.io/) is a good alternative if you want to use a vector database.

Unitl now, training has been finished but the indexing and searching part only uses a small sample dataset as I want the interviewer to run the code on their machine and see the results. It takes time to share a parquet file with 1.5M records and its embeddings.

If you haven't tried [onnx](https://onnx.ai/) before, please check it out. It is a great way to deploy your models in production if you care about performance in production.



## Running Requirements

- Python3.10.10
- Docker (>24.0.5 should work)
- Docker-compose


## Installation

```sh
# check your python version
# recommend using pyenv to manage python versions
python --V  # should be >= 3.10.10
python -m venv venv
source venv/bin/activate
make install
```

## Runnning Localhost

1. `make onnx`: construct [onnx](https://onnx.ai/) model
2. `make elastic-up`: start [Elasticsearch](https://www.elastic.co/elasticsearch/)
3. `make index-books`: index books (_might need to run this several times as elasticsearch might not be ready_)
4. `make run`: start FastAPI server


## Running Tests

`make test`

## Access Swagger Documentation

**The port might be different if you have already running services on port 8080**

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Deploy app

TODO: Add deployment instructions

## Project structure

It uses fastapi-cookiecutter template. The project structure is as follows:

    .
    ├── app
    │   ├── api
    │   ├── core
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models
    │   ├── __pycache__
    │   ├── services
    │   └── templates
    ├── docker-compose.yml
    ├── Dockerfile
    ├── Makefile
    ├── ml
    │   ├── data
    │   ├── features
    │   ├── __init__.py
    │   ├── model
    │   └── __pycache__
    ├── notebooks
    │   ├── construct_sample_dataset.ipynb
    │   └── onnx_runtime.ipynb
    ├── poetry.lock
    ├── pyproject.toml
    ├── README.md
    ├── search
    │   ├── books_embeddings.csv
    │   ├── docker-compose.yml
    │   └── index_books.py
    ├── tests
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── test_api.py
    │   ├── test_elastic_search.py
    │   └── test_onnx_embedding.py



### Data Source


Originally, the data is downloaded from [Goodreads Book Graph Datasets](https://mengtingwan.github.io/data/goodreads.html). The author also provides the [code](https://github.com/MengtingWan/goodreads?tab=readme-ov-file) to download the data.

I downloaded the data and uploaded it to my Google Cloud Storage bucket. Please let me know if you found above links are broken and I will provide you with the data.

There are many tables in the dataset, but we are only interested in the following tables:

- books:  detailed meta-data about 2.36M books
- reviews: Complete 15.7m reviews (~5g) and 15M records with detailed review text