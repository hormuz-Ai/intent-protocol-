from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    origin = params.get('origin', 'Shanghai')
    destination = params.get('destination', 'Rotterdam')
    containers = params.get('containers', 1)

    rate_per_container = 4500
    total = containers * rate_per_container

    return jsonify({
        "status": "fulfilled",
        "value": total,
        "currency": "USD",
        "provider": "INTP Freight Solver (Freightos bridge)",
        "details": f"Ship {containers} container(s) {origin} → {destination}: ${total}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
