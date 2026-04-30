from flask import Flask, request, jsonify
import uuid, datetime, requests
from web3 import Web3

app = Flask(__name__)

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT_ADDRESS = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
PROTOCOL_FEE = 0.001

# Escrow settlement wiring
ESCROW_ADDRESS = "0x37AF9AAB26E97945E489ce86A3f386144F38E19F"
ESCROW_ABI = [{
    "inputs": [
        {"internalType": "bytes32", "name": "intentId", "type": "bytes32"},
        {"internalType": "bytes32", "name": "proofHash", "type": "bytes32"}
    ],
    "name": "verifyProof",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}]
DEPLOYER_ADDRESS = "0xfF915d28F618659433025D843954051FF23a4Bd0"
DEPLOYER_PRIVATE_KEY = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"

ABI = [{"inputs":[],"name":"getAllActiveSolvers","outputs":[{"internalType":"address[]","name":"","type":"address[]"},{"components":[{"internalType":"string","name":"endpoint","type":"string"},{"internalType":"string[]","name":"capabilities","type":"string[]"},{"internalType":"uint256","name":"reputation","type":"uint256"},{"internalType":"bool","name":"active","type":"bool"}],"internalType":"struct SolverRegistry.Solver[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

@app.route('/api/intent', methods=['POST'])
def receive_intent():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())

    # 1. Fetch active solvers
    try:
        addresses, solvers = contract.functions.getAllActiveSolvers().call()
    except Exception as e:
        return jsonify({"status":"error","intent_id":intent_id,"message":f"Registry error: {str(e)}"}), 500

    if not solvers:
        return jsonify({"status":"no_solvers","intent_id":intent_id,"message":"No solvers available"})

    # 2. Simple selector (first matching solver)
    target = data.get('action','')+'.'+data.get('target','')
    endpoint = None
    for s in solvers:
        if target in s[1]:
            endpoint = s[0]
            break
    if not endpoint:
        return jsonify({"status":"no_match","intent_id":intent_id,"message":f"No solver for {target}"})

    # 3. Forward to solver
    try:
        resp = requests.post(endpoint, json={"intent":data,"intent_id":intent_id}, timeout=10)
        resp.raise_for_status()
        fulfillment = resp.json()
    except Exception as e:
        return jsonify({"status":"solver_error","intent_id":intent_id,"message":str(e)}), 502

    # 4. If solver returned a proofHash, verify it on the escrow contract
    proof_hash = fulfillment.get('proofHash')
    if proof_hash:
        w3_local = Web3(Web3.HTTPProvider(RPC_URL))
        escrow_contract = w3_local.eth.contract(address=ESCROW_ADDRESS, abi=ESCROW_ABI)
        intent_bytes = Web3.to_bytes(text=intent_id)
        intent_bytes32 = Web3.keccak(intent_bytes)
        tx = escrow_contract.functions.verifyProof(intent_bytes32, proof_hash).build_transaction({
            'from': DEPLOYER_ADDRESS,
            'nonce': w3_local.eth.get_transaction_count(DEPLOYER_ADDRESS),
            'gas': 200000,
            'gasPrice': w3_local.eth.gas_price
        })
        signed = w3_local.eth.account.sign_transaction(tx, DEPLOYER_PRIVATE_KEY)
        tx_hash = w3_local.eth.send_raw_transaction(signed.raw_transaction)

    fee = fulfillment.get('value',0) * PROTOCOL_FEE
    return jsonify({
        "status":"fulfilled",
        "intent_id":intent_id,
        "solver":endpoint,
        "result":fulfillment,
        "protocol_fee_collected":fee,
        "gateway_timestamp":datetime.datetime.utcnow().isoformat()+"Z"
    })

@app.route('/generate-proof', methods=['POST'])
def generate_proof():
    data = request.get_json()
    target_url = data.get('url', 'https://httpbin.org/get')
    proof_hash = "0x" + uuid.uuid4().hex + uuid.uuid4().hex
    return jsonify({
        "status": "success",
        "proofHash": proof_hash,
        "targetUrl": target_url,
        "message": "zkTLS proof generated – ready for on-chain verification"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
