import pytest
from ml.model.embedding_generator import ONNXEmbeddingGenerator

def test_onnx_embeddings():
    generator = ONNXEmbeddingGenerator()
    embeddings = generator.generate_embeddings(["hello world"])
    assert list(embeddings[0].shape) == [1, 768]
    embeddings = generator.generate_embeddings(["hello world", "goodbye world"])
    assert len(embeddings) == 2