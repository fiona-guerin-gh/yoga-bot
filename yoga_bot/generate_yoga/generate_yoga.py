from flask import Flask, render_template, request
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def render_web():
    return render_template('yoga_bot.html')

@app.route('/generate', methods=['POST'])
def generate_yoga():
    yoga_type = request.form['YogaType']

    # Update yoga request tracker
    yoga_request_tracker = json.loads(redis.get('yoga_request_tracker') or '{}') 
    yoga_request_tracker[yoga_type] = yoga_request_tracker.get(yoga_type, 0) + 1
    redis.set('yoga_request_tracker', json.dumps(yoga_request_tracker))
    print(f'There are {yoga_request_tracker[yoga_type]} requests to generate a new {yoga_type} flow.')

    # Get yoga flows and next flow index
    yoga_flows = json.loads(redis.get('yoga_flows') or '{}')
    next_yoga_flows = json.loads(redis.get('next_yoga_flows') or '{}')
    yoga_flow_index = min(next_yoga_flows.get(yoga_type, 0), len(yoga_flows.get(yoga_type, [])) - 1)
    print(f'Presenting yoga flow #{yoga_flow_index}.')

    # Update next flow index
    next_yoga_flows[yoga_type] = yoga_flow_index + 1
    redis.set('next_yoga_flows', json.dumps(next_yoga_flows))

    # Render template with selected yoga flow
    return render_template('yoga_bot.html', yoga_flow=yoga_flows[yoga_type][yoga_flow_index])

if __name__ == '__main__':
    app.run(port=5002)
