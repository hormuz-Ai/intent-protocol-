from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    gpu = params.get('gpu', 'H100')
    hours = params.get('hours', 1)
    return jsonify({
        "status": "fulfilled",
        "value": hours * 2.50,
        "currency": "USD",
        "provider": "INTP Compute Solver",
        "details": f"Rent {gpu} for {hours}h at ~$2.50/h"
    })
