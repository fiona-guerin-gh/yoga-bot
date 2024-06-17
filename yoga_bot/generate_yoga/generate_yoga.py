from flask import Flask, render_template, request
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, decode_responses=True)

    
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

if __name__ == '__main__':
    app.run(port=5001)
