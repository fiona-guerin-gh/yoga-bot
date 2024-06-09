import os
import pathlib
import sys

PACKAGE_ROOT = pathlib.Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from yoga_bot.config import config
from yoga_bot.processing.data_handling import load_model

def predict():
    llm = load_model()
    response = llm(config.PROMPT, max_tokens=1000)
    response_text = response['choices'][0]['text']
    print(response_text)
    return response_text


if __name__ == '__main__':
    predict()
