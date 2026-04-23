from flask import Flask, request, jsonify
import uuid, datetime, requests
from web3 import Web3

app = Flask(__name__)

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT_ADDRESS = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
PROTOCOL_FEE = 0.001

# ABI that works with the deployed contract
ABI = [
    "function getAllActiveSolvers() external view returns (address[] memory, tuple(string,string[],uint256,bool)[] memory)"
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

@app.route('/api/intent', methods=['POST'])
def handle():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())
    try:
        addrs, solvers = contract.functions.getAllActiveSolvers().call()
    except Exception as e:
        # fallback: if the call fails, hardcode the solver
        print(f"Contract call failed: {e}, using hardcoded solver")
        endpoint = "https://solver-deploy.vercel.app/a2a"
    else:
        if not solvers:
            # still fallback
            endpoint = "https://solver-deploy.vercel.app/a2a"
        else:
            # find first solver with matching capability
            target = data.get('action','')+'.'+data.get('target','')
            endpoint = None
            for s in solvers:
                if target in s[1]:
                    endpoint = s[0]
                    break
            if not endpoint:
                return jsonify({"status":"no_match","intent_id":intent_id,"message":f"No solver for {target}"})

    # Forward intent to solver
    try:
        resp = requests.post(endpoint, json={"intent":data,"intent_id":intent_id}, timeout=10)
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
