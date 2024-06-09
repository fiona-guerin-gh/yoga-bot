import os
import pathlib
import sys

from huggingface_hub import hf_hub_download
from llama_cpp import Llama

PACKAGE_ROOT = pathlib.Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from yoga_bot.config import config, token

def instantiate_model():
    model_path = hf_hub_download(config.MODEL_NAME,
                             filename=config.MODEL_FILE,
                             local_dir=config.MODEL_PATH,
                             token=token.HF_TOKEN)
    print(f'Loded model at path {model_path}.')
    llm = Llama(model_path=model_path, n_gpu_layers=-1)
    return llm


if __name__ == '__main__':
    instantiate_model()
