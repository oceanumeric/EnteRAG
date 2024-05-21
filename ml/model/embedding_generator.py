import os
import timeit
from typing import List
from pathlib import Path

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer
from sentence_embedding_pipeline import SentenceEmbeddingPipeline


current_dir = os.path.dirname(os.path.abspath(__file__))

class ONNXEmbeddingGenerator:
    def __init__(self):
        self.onnx_path = os.path.join(current_dir, "sentence-transformers/msmarco-distilbert-base-tas-b.onnx")
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

    


