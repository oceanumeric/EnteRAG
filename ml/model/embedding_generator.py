import os
import timeit
from typing import List
from pathlib import Path

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer
from sentence_embedding_pipeline import SentenceEmbeddingPipeline


def get_project_root():
    # Starting directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # List of marker files or directories that indicate the project root
    markers = ['Makefile', 'pyproject.toml']

    # Traverse up the directory tree until a marker is found
    while current_dir:
        if any(os.path.exists(os.path.join(current_dir, marker)) for marker in markers):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        # Break if we've reached the root directory
        if parent_dir == current_dir:
            break
        current_dir = parent_dir

    # If no marker is found, default to the directory containing the current script
    return os.path.abspath(os.path.dirname(__file__))

project_root = get_project_root()

class ONNXEmbeddingGenerator:
    def __init__(self):
        self.onnx_path = os.path.join(project_root, "sentence-transformers/msmarco-distilbert-base-tas-b.onnx")
        self.model = ORTModelForFeatureExtraction.from_pretrained(self.onnx_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.onnx_path)
        self.pipeline = SentenceEmbeddingPipeline(model=self.model, tokenizer=self.tokenizer)

    def generate_embeddings(self, inputs: List[str]):
        embeddings = self.pipeline(inputs)
        return embeddings
    

if __name__ == "__main__":
    # test the ONNXEmbeddingGenerator
    st_time = timeit.default_timer()
    generator = ONNXEmbeddingGenerator()
    embeddings = generator.generate_embeddings(["hello world"])
    print(embeddings[0].shape)
    print(f"Time taken: {timeit.default_timer() - st_time} seconds.")

    


