from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"
PROVIDER_URL = "YOUR_PROVIDER_URL"

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    intent_id = data.get('intent_id')
    action = intent.get('action', '')
    target = intent.get('target', '')
    params = intent.get('params', {})

    # TODO: Add your fulfillment logic here
    # 1. Call your service API
    # 2. Extract the price and details
    # 3. Return the result

    return jsonify({
        "status": "fulfilled",
        "value": 0,
        "currency": "USD",
        "provider": "test-solver",
        "details": f"Fulfilled {action}.{target} with params {params}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
