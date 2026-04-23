from flask import Flask, request, jsonify
import uuid, datetime, requests
from web3 import Web3

app = Flask(__name__)

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT_ADDRESS = "0x9D7d47848cb11724E08456E525182246057B3f"
PROTOCOL_FEE_PERCENT = 0.001

CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "getAllActiveSolvers",
        "outputs": [
            {"internalType": "address[]", "name": "", "type": "address[]"},
            {
                "components": [
                    {"internalType": "string", "name": "endpoint", "type": "string"},
                    {"internalType": "string[]", "name": "capabilities", "type": "string[]"},
                    {"internalType": "uint256", "name": "reputation", "type": "uint256"},
                    {"internalType": "bool", "name": "active", "type": "bool"}
                ],
                "internalType": "struct SolverRegistry.Solver[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def select_best_solver(intent, solvers_data):
    target = intent.get('target', '')
    action = intent.get('action', '')
    required_capability = f"{action}.{target}"
    best_endpoint = None
    best_reputation = -1
    for solver in solvers_data:
        if required_capability in solver[1]:
            if solver[2] > best_reputation:
                best_reputation = solver[2]
                best_endpoint = solver[0]
    return best_endpoint

@app.route('/api/intent', methods=['POST'])
def receive_intent():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())
    try:
        addresses, solvers = contract.functions.getAllActiveSolvers().call()
    except Exception as e:
        return jsonify({"status":"error","intent_id":intent_id,"message":f"Registry error: {str(e)}"}), 500
    if not solvers:
        return jsonify({"status":"no_solvers","intent_id":intent_id,"message":"No solvers available"})
    solver_data = [(s[0], s[1], s[2]) for s in solvers]
    endpoint = select_best_solver(data, solver_data)
    if not endpoint:
        return jsonify({"status":"no_matching_solver","intent_id":intent_id,"message":f"No solver supports {data.get('action')}.{data.get('target')}"})
    try:
        solver_resp = requests.post(endpoint, json={"intent": data, "intent_id": intent_id}, timeout=10)
        solver_resp.raise_for_status()
        fulfillment = solver_resp.json()
    except Exception as e:
        return jsonify({"status":"solver_error","intent_id":intent_id,"message":f"Solver failed: {str(e)}"}), 502
    transaction_value = fulfillment.get('value', 0)
    protocol_fee = transaction_value * PROTOCOL_FEE_PERCENT
    return jsonify({
        "status": "fulfilled",
        "intent_id": intent_id,
        "solver": endpoint,
        "result": fulfillment,
        "protocol_fee_collected": protocol_fee,
        "gateway_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
