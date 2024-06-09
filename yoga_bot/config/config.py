import pathlib
import os
import yoga_bot

PACKAGE_ROOT = pathlib.Path(yoga_bot.__file__).resolve().parent

MODEL_NAME = 'google/gemma-2b-it'
MODEL_FILE = 'gemma-2b-it.gguf'
MODEL_PATH = os.path.join(PACKAGE_ROOT, 'model')

PROMPT = """Create a 30 minute long sequence of yoga poses that specifically targets flexibility and relaxation. Include a mix of standing, seated, and supine poses, along with recommended breathwork and mindfulness techniques:"""
