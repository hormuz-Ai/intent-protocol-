from flask import Flask, request, jsonify
import uuid
import datetime

app = Flask(__name__)

@app.route('/api/intent', methods=['POST'])
def receive_intent():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())
    return jsonify({
        "status": "received",
        "intent_id": intent_id,
        "estimated_fulfillment": "pending_solver_assignment",
        "gateway_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
