from concurrent.futures import ThreadPoolExecutor
from config import config, token
from redis import Redis
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import json
import mlflow
from random import randint
import matplotlib.pyplot as plt

redis = Redis(host='localhost', port=6379, decode_responses=True)

mlflow.set_experiment("Yoga Bot")

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

if False:  #torch.backends.mps.is_available():
    print('mps is used.')
    device_name = 'mps'
elif torch.cuda.is_available():
    print('cuda is used.')
    device_name = 'cuda'
else:
    print('CPU is used.')
    device_name = 'cpu'
device = torch.device(device_name)

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, token=token.HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(config.MODEL_NAME, token=token.HF_TOKEN, torch_dtype=torch.bfloat16)
model.to(device)

def call_model():
    prompt_tags = []
    max_new_tokens_list = []
    temperatures = []
    inference_times = []
    dev_ratings = []
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
            default_prompt = f'{config.PROMPT}{yoga_type}'
            one_shot_sample = json.loads(redis.get('yoga_flows'))[yoga_type][0]
            one_shot_prompt = f'Here is an example yoga flow: {one_shot_sample}.\n{default_prompt}'
            few_shot_sample = ' Here is an example yoga flow: '.join(json.loads(redis.get('yoga_flows'))[yoga_type])
            few_shot_prompt = f'Here is an example yoga flow: {few_shot_sample}.\n{default_prompt}'
            prompts = [('default_prompt', default_prompt), ('one_shot_prompt', one_shot_prompt), ('few_shot_prompt', few_shot_prompt)]
            for k in range (0, 10):
                for i, (prompt_tag, prompt) in enumerate(prompts):
                    with mlflow.start_run():
                        mlflow.set_tag("prompt", prompt_tag)
                        prompt_tags.append(i)
                        mlflow.log_metric('prompt_length', len(prompt))
                        input_ids = tokenizer(prompt, return_tensors='pt').to(device_name)
                        max_new_tokens=randint(100, 1000)
                        mlflow.log_metric('max_new_tokens', max_new_tokens)
                        max_new_tokens_list.append(max_new_tokens)
                        temperature=randint(1, 10) / 10.0
                        mlflow.log_metric('temperature', temperature)
                        temperatures.append(temperature)
                        print('Calling model...')
                        start_time = time.time()
                        outputs = model.generate(
                            **input_ids, 
                            max_new_tokens=max_new_tokens,
                            do_sample=True,
                            temperature=temperature,
                        )
                        end_time = time.time()
                        inference_time = end_time-start_time
                        print(f'Called model; elapsed time: {inference_time}')
                        mlflow.log_metric('inference_time', inference_time)
                        inference_times.append(inference_time)
                        response_text = tokenizer.decode(outputs[0])
                        response_text = response_text.replace(prompt, '')
                        print(f'The response is {response_text}.')
                        mlflow.set_tag('response_text', response_text)

                        dev_rating = int(input('How good is the generated yoga flow?'))
                        mlflow.log_metric('user_rating', dev_rating)
                        dev_ratings.append(dev_rating)
                        
                        if dev_rating > 0:
                            yoga_flows = json.loads(redis.get('yoga_flows'))
                            yoga_flows[yoga_type].append(response_text)
                            redis.set('yoga_flows', json.dumps(yoga_flows))
                            print('Updated yoga flows on Redis.')
                        else:
                            print('The generated response is not an acceptable yoga flow. Discarding...')

                        yoga_request_tracker = json.loads(redis.get('yoga_request_tracker'))
                        yoga_requests = int(yoga_request_tracker[yoga_type]) - 1
                        yoga_request_tracker[yoga_type] = yoga_requests
                        redis.set('yoga_request_tracker', json.dumps(yoga_request_tracker))
                        print(prompt_tags)
                        print(max_new_tokens_list)
                        print(temperatures)
                        print(inference_times)
                        print(dev_ratings)
                        plt.scatter(temperatures, dev_ratings)
                        plt.show()
                        plt.scatter(max_new_tokens_list, dev_ratings)
                        plt.show()
                        plt.scatter(prompt_tags, dev_ratings)
                        plt.show()
                        plt.scatter(temperatures, inference_times)
                        plt.show()
                        plt.scatter(max_new_tokens_list, inference_times)
                        plt.show()
                        plt.scatter(prompt_tags, inference_times)
                        plt.show()

call_model()