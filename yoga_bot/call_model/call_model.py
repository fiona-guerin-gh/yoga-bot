from config import config, token
from redis import Redis
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import json

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
