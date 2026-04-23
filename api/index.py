from flask import Flask, request, jsonify
import uuid, datetime, requests

app = Flask(__name__)

SOLVER_ENDPOINT = "https://solver-deploy.vercel.app/a2a"
PROTOCOL_FEE = 0.001

@app.route('/api/intent', methods=['POST'])
def handle():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())

    # Forward intent directly to the solver
    try:
        resp = requests.post(SOLVER_ENDPOINT, json={"intent": data, "intent_id": intent_id}, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        return jsonify({"status": "solver_error", "intent_id": intent_id, "message": str(e)}), 502

    fee = result.get('value', 0) * PROTOCOL_FEE
    return jsonify({
        "status": "fulfilled",
        "intent_id": intent_id,
        "solver": SOLVER_ENDPOINT,
        "result": result,
        "protocol_fee_collected": fee,
        "gateway_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
