from concurrent.futures import ThreadPoolExecutor
from yoga_bot.config import config, token
from flask import Flask,render_template,request
from redis import Redis
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, decode_responses=True)

#if not redis.exists('yoga_flows'):
redis.set('yoga_flows', json.dumps({
    'Vinyasa Yoga': [config.VINYASA_EXAMPLE],
    'Yin Yoga': [config.YIN_EXAMPLE],
    'Power Yoga': [config.POWER_EXAMPLE],
}))
#if not redis.exists('next_yoga_flows'):
redis.set('next_yoga_flows', json.dumps({
    'Vinyasa Yoga': 0,
    'Yin Yoga': 0,
    'Power Yoga': 0,
}))
#if not redis.exists('yoga_request_tracker'):
redis.set('yoga_request_tracker', json.dumps({
    'Vinyasa Yoga': 0,
    'Yin Yoga': 0,
    'Power Yoga': 0,
}))

if False: # torch.backends.mps.is_available():
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
    
@app.route('/')
def render_web():
    return render_template('yoga_bot.html')

@app.route('/generate',methods=['POST'])
def generate_yoga():
    request_data = dict(request.form)
    yoga_type = request_data['YogaType']
    
    yoga_request_tracker = json.loads(redis.get('yoga_request_tracker'))
    yoga_requests = int(yoga_request_tracker[yoga_type]) + 1
    yoga_request_tracker[yoga_type] = yoga_requests
    redis.set('yoga_request_tracker', json.dumps(yoga_request_tracker))
    print(f'There are {yoga_requests} requests to generate a new {yoga_type} flow.')
    
    yoga_flows = json.loads(redis.get('yoga_flows'))
    next_yoga_flows = json.loads(redis.get('next_yoga_flows'))
    yoga_flow_index = min(int(next_yoga_flows[yoga_type]), len(yoga_flows[yoga_type])-1)
    print(f'Presenting yoga flow #{yoga_flow_index}.')
    next_yoga_flows[yoga_type] = yoga_flow_index + 1
    redis.set('next_yoga_flows', json.dumps(next_yoga_flows))
    return render_template('yoga_bot.html', yoga_flow=yoga_flows[yoga_type][yoga_flow_index])

def call_model():
    while True:
        yoga_type = ''
        yoga_request_tracker = json.loads(redis.get('yoga_request_tracker'))
        for yoga_request_type, yoga_request_count in yoga_request_tracker.items():
            if int(yoga_request_count) > 0:
                yoga_type = yoga_request_type
        if not yoga_type:
            print('No new yoga requests. Going to sleep ...')
            time.sleep(10)
        else:
            print(f'Generating a novel {yoga_type} flow.')
            prompt = f'{config.PROMPT}{yoga_type}'
            input_ids = tokenizer(prompt, return_tensors='pt').to(device_name)
            outputs = model.generate(
                **input_ids,
                max_new_tokens=1000,
            )
            response_text = tokenizer.batch_decode(outputs[:, input_ids['input_ids'].shape[0]:])[0]
            yoga_flows = json.loads(redis.get('yoga_flows'))
            yoga_flows[yoga_type].append(response_text)
            
            redis.set('yoga_flows', json.dumps(yoga_flows))
            print(response_text)


if __name__ == '__main__':
    app.run(debug=True, port=8001)
