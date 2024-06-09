import os
from llama_cpp import Llama
from yoga_bot.config import config


def load_model():
    model_path = os.path.join(config.MODEL_PATH, config.MODEL_FILE)
    llm = Llama(model_path=model_path, n_gpu_layers=-1)
    return llm
