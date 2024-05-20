SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

ifeq ($(MODEL_PATH),)
MODEL_PATH := ./ml/model/
endif

ifeq ($(MODEL_NAME),)
MODEL_NAME := model.pkl
endif

ifeq ($(ONNX_FILE_PATH),)
ONNX_FILE_PATH := ./ml/model/sentence-transformers/msmarco-distilbert-base-tas-b.onnx
endif

# Target section and Global definitions
# -----------------------------------------------------------------------------
.PHONY: all clean test install run deploy down

all: clean test install run deploy down

test:
	poetry run pytest tests -vv --show-capture=all

install: generate_dot_env
	pip install --upgrade pip
	pip install poetry
	poetry install --with dev

onnx:
	@if [[ ! -d $(ONNX_FILE_PATH) ]]; then \
		echo "Creating ONNX file path: $(ONNX_FILE_PATH)"; \
		mkdir -p $(ONNX_FILE_PATH); \
	fi
	poetry run python ml/model/onnx_runtime.py $(ONNX_FILE_PATH)

run:
	PYTHONPATH=app/ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 5758

deploy: generate_dot_env
	docker-compose build
	docker-compose up -d

down:
	docker-compose down

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build