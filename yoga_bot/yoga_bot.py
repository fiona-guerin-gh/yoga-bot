from concurrent.futures import ThreadPoolExecutor
from config import config, token
from flask import Flask,render_template,request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

if False and torch.backends.mps.is_available():
    print('mps is used.')
    device_name = 'mps'
elif torch.cuda.is_available():
    print('cuda is used.')
    device_name = 'cuda'
else:
    print('cpu is used.')
    device_name = 'cpu'
device = torch.device(device_name)

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, token=token.HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(config.MODEL_NAME, token=token.HF_TOKEN)
model.to(device)

yoga_flows = {
    'Vinyasa Yoga': [config.VINYASA_EXAMPLE],
    'Yin Yoga': [config.YIN_EXAMPLE],
    'Power Yoga': [config.POWER_EXAMPLE],
}
    
@app.route('/')
def render_web():
    return render_template('yoga_bot.html')

@app.route('/generate',methods=['POST'])
def generate_yoga():
    request_data = dict(request.form)
    yoga_type = request_data['YogaType']
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda _: call_model(yoga_type))
        print(future.result())
    return render_template('yoga_bot.html', yoga_flow=yoga_flows[yoga_type][-1])

async def call_model(yoga_type):
    prompt = f'{config.PROMPT}{yoga_type}'
    input_ids = tokenizer(prompt, return_tensors='pt').to(device_name)
    outputs = model.generate(
        **input_ids,
        max_new_tokens=1000,
        )
    response_text = tokenizer.batch_decode(outputs[:, input_ids['input_ids'].shape[1]:])[0]
    yoga_flows[yoga_type].append(response_text)
    return response_text


if __name__ == '__main__':
    app.run(debug=True, port=8001)
