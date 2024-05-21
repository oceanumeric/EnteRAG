# EnteRAG

AI-powered Enterprise RAG

## Development Requirements

- Python3.10.10
- Docker
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

1. construct [onnx](https://onnx.ai/) model
    `make onnx`
2. start [Elasticsearch](https://www.elastic.co/elasticsearch/)
    `make elastic-up`
3. index books
    `make index-books`
4. start FastAPI server
    `make run`


## Deploy app

TODO: Add deployment instructions

## Running Tests

`make test`

## Access Swagger Documentation

**The port might be different if you have already running services on port 8080**

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

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