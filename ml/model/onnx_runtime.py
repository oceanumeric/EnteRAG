import click
from pathlib import Path

from loguru import logger

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer
from pathlib import Path


def pipeline(path: str):
    logger.info("Start converting model to onnx.")
    model_id="sentence-transformers/msmarco-distilbert-base-tas-b"
    onnx_path = Path(path)
 
    # load vanilla transformers and convert to onnx 
    model = ORTModelForFeatureExtraction.from_pretrained(model_id, from_transformers=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # save onnx checkpoint and tokenizer
    model.save_pretrained(onnx_path)
    tokenizer.save_pretrained(onnx_path)
    
    
@click.command()
@click.argument("output_filepath", default="sentence-transformers/msmarco-distilbert-base-tas-b.onnx", type=click.Path(exists=True))
def main(output_filepath):
    """Generate onnx model from huggingface model."""
    logger.info(f"onnx model will be saved to {output_filepath}.")
    pipeline(output_filepath)
    

if __name__ == "__main__":
    main()
    