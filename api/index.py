from flask import Flask, request, jsonify
import uuid, datetime, requests
from web3 import Web3

app = Flask(__name__)

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT_ADDRESS = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
PROTOCOL_FEE = 0.001

# Minimal ABI that exactly matches the deployed contract
ABI = [{
    "inputs": [],
    "name": "getAllActiveSolvers",
    "outputs": [
        {"internalType": "address[]", "name": "", "type": "address[]"},
        {"components": [
            {"internalType": "string", "name": "endpoint", "type": "string"},
            {"internalType": "string[]", "name": "capabilities", "type": "string[]"},
            {"internalType": "uint256", "name": "reputation", "type": "uint256"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ], "internalType": "struct SolverRegistry.Solver[]", "name": "", "type": "tuple[]"}
    ],
    "stateMutability": "view",
    "type": "function"
}]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

@app.route('/api/intent', methods=['POST'])
def handle():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())

    try:
        addresses, solvers = contract.functions.getAllActiveSolvers().call()
    except Exception as e:
        # Fallback: use the known solver if contract call fails
        endpoint = "https://solver-deploy.vercel.app/a2a"
    else:
        if not solvers or len(solvers) == 0:
            endpoint = "https://solver-deploy.vercel.app/a2a"
        else:
            # Find first solver matching the intent
            target = data.get('action','') + '.' + data.get('target','')
            endpoint = None
            for s in solvers:
                if target in s[1]:  # capabilities array
                    endpoint = s[0]
                    break
            if not endpoint:
                endpoint = solvers[0][0]  # fallback to first solver

    try:
        resp = requests.post(endpoint, json={"intent": data, "intent_id": intent_id}, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        return jsonify({"status":"solver_error","intent_id":intent_id,"message":str(e)}),502

    fee = result.get('value',0) * PROTOCOL_FEE
    return jsonify({
        "status":"fulfilled",
        "intent_id":intent_id,
        "solver":endpoint,
        "result":result,
        "protocol_fee_collected":fee,
        "gateway_timestamp":datetime.datetime.utcnow().isoformat()+"Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
