from config import config, token
from redis import Redis
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import json
import mlflow
from random import randint

# Redis setup
redis = Redis(host='localhost', port=6379, decode_responses=True)

# MLflow experiment setup
mlflow.set_experiment("Yoga Bot")

# Initialize Redis keys if they don't exist (assuming this is the intended behavior)
initial_yoga_flows = {
    'Vinyasa Yoga': [config.VINYASA_EXAMPLE],
    'Yin Yoga': [config.YIN_EXAMPLE],
    'Power Yoga': [config.POWER_EXAMPLE],
}
initial_next_yoga_flows = {
    'Vinyasa Yoga': 0,
    'Yin Yoga': 0,
    'Power Yoga': 0,
}
initial_yoga_request_tracker = {
    'Vinyasa Yoga': 0,
    'Yin Yoga': 0,
    'Power Yoga': 0,
}

for key, value in [
    ('yoga_flows', initial_yoga_flows),
    ('next_yoga_flows', initial_next_yoga_flows),
    ('yoga_request_tracker', initial_yoga_request_tracker),
]:
    if not redis.exists(key):
        redis.set(key, json.dumps(value))

# Device selection (simplified)
# Replace `False` with `torch.backends.mps.is_available()`
device_name = 'mps' if False else 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'{device_name} is used.')
device = torch.device(device_name)

# Model loading
tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, token=token.HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    config.MODEL_NAME, token=token.HF_TOKEN, torch_dtype=torch.bfloat16
)
model.to(device)

def call_model():
    while True:
        # Check for new yoga requests
        yoga_type = next(
            (
                yoga_request_type
                for yoga_request_type, yoga_request_count in json.loads(
                    redis.get('yoga_request_tracker')
                ).items()
                if int(yoga_request_count) > 0
            ),
            None,
        )

        if not yoga_type:
            print('No new yoga requests. Going to sleep ...')
            time.sleep(10)
            continue  # Continue to the next iteration of the loop

        print(f'Generating a novel {yoga_type} flow.')

        # Prompt construction
        default_prompt = f'{config.PROMPT}{yoga_type}'
        yoga_flows = json.loads(redis.get('yoga_flows'))[yoga_type]
        one_shot_prompt = f'Here is an example yoga flow: {yoga_flows[0]}.\n{default_prompt}'
        few_shot_prompt = f'Here is an example yoga flow: {" Here is an example yoga flow: ".join(yoga_flows)}.\n{default_prompt}'
        prompts = [
            ('default_prompt', default_prompt),
            ('one_shot_prompt', one_shot_prompt),
            ('few_shot_prompt', few_shot_prompt),
        ]

        for _ in range(10):  # Assuming you want to generate 10 flows per request
            for i, (prompt_tag, prompt) in enumerate(prompts):
                with mlflow.start_run():
                    mlflow.set_tag("prompt", prompt_tag)
                    mlflow.log_metric('prompt_length', len(prompt))

                    # Model inference
                    input_ids = tokenizer(prompt, return_tensors='pt').to(device_name)
                    max_new_tokens = randint(100, 1000)
                    temperature = randint(1, 10) / 10.0
                    mlflow.log_metrics(
                        {
                            'max_new_tokens': max_new_tokens,
                            'temperature': temperature,
                        }
                    )

                    print('Calling model...')
                    start_time = time.time()
                    outputs = model.generate(
                        **input_ids,
                        max_new_tokens=max_new_tokens,
                        do_sample=True,
                        temperature=temperature,
                    )
                    end_time = time.time()
                    inference_time = end_time - start_time
                    print(f'Called model; elapsed time: {inference_time}')
                    mlflow.log_metric('inference_time', inference_time)

                    # Response processing
                    response_text = tokenizer.decode(outputs[0]).replace(prompt, '')
                    print(f'The response is {response_text}.')
                    mlflow.set_tag('response_text', response_text)

                    # User feedback and Redis update
                    dev_rating = int(input('How good is the generated yoga flow?'))
                    mlflow.log_metric('user_rating', dev_rating)

                    if dev_rating > 0:
                        yoga_flows.append(response_text)
                        redis.set('yoga_flows', json.dumps(yoga_flows))
                        print('Updated yoga flows on Redis.')
                    else:
                        print('The generated response is not an acceptable yoga flow. Discarding...')

                    # Update request tracker
                    yoga_request_tracker = json.loads(redis.get('yoga_request_tracker'))
                    yoga_request_tracker[yoga_type] -= 1
                    redis.set('yoga_request_tracker', json.dumps(yoga_request_tracker))

# Start the model generation loop
call_model()