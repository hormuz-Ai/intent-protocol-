from reclaim_python_sdk import ReclaimProofRequest
import os


from flask import Flask, request, jsonify
import uuid, datetime, requests
from web3 import Web3

app = Flask(__name__)

RPC_URL = 'https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN'
CONTRACT_ADDRESS = '0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25'
PROTOCOL_FEE = 0.001
ESCROW_ADDRESS = '0x37AF9AAB26E97945E489ce86A3f386144F38E19F'
ESCROW_ABI = [{"inputs":[{"internalType":"bytes32","name":"intentId","type":"bytes32"},{"internalType":"bytes32","name":"proofHash","type":"bytes32"}],"name":"verifyProof","outputs":[],"stateMutability":"nonpayable","type":"function"}]
DEPLOYER_ADDRESS = '0xfF915d28F618659433025D843954051FF23a4Bd0'
DEPLOYER_PRIVATE_KEY = '0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7'

ABI = [{"inputs":[],"name":"getAllActiveSolvers","outputs":[{"internalType":"address[]","name":"","type":"address[]"},{"components":[{"internalType":"string","name":"endpoint","type":"string"},{"internalType":"string[]","name":"capabilities","type":"string[]"},{"internalType":"uint256","name":"reputation","type":"uint256"},{"internalType":"bool","name":"active","type":"bool"}],"internalType":"struct SolverRegistry.Solver[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

@app.route('/api/intent', methods=['POST'])
def receive_intent():
    data = request.get_json()
    intent_id = data.get('intent_id') or str(uuid.uuid4())
    try:
        addresses, solvers = contract.functions.getAllActiveSolvers().call()
    except Exception as e:
        return jsonify({'status':'error','intent_id':intent_id,'message':f'Registry error: {str(e)}'}), 500
    if not solvers:
        return jsonify({'status':'no_solvers','intent_id':intent_id,'message':'No solvers available'})
    target = data.get('action','')+'.'+data.get('target','')
    endpoint = None
    for s in solvers:
        if target in s[1]:
            endpoint = s[0]
            break
    if not endpoint:
        return jsonify({'status':'no_match','intent_id':intent_id,'message':f'No solver for {target}'})
    try:
        resp = requests.post(endpoint, json={'intent':data,'intent_id':intent_id}, timeout=10)
        resp.raise_for_status()
        fulfillment = resp.json()
    except Exception as e:
        return jsonify({'status':'solver_error','intent_id':intent_id,'message':str(e)}), 502
    fee = fulfillment.get('value',0) * PROTOCOL_FEE
    return jsonify({'status':'fulfilled','intent_id':intent_id,'solver':endpoint,'result':fulfillment,'protocol_fee_collected':fee,'gateway_timestamp':datetime.datetime.utcnow().isoformat()+'Z'})

@app.route('/generate-proof', methods=['POST'])
def generate_proof():
    import asyncio
    async def _get():
        proof_request = await ReclaimProofRequest.init(
            app_id=os.environ.get('RECLAIM_APP_ID'),
            app_secret=os.environ.get('RECLAIM_APP_SECRET'),
            provider_id=os.environ.get('RECLAIM_PROVIDER_ID'),
        )
        proof_request.set_app_callback_url(
            'https://intent-protocol-xi.vercel.app/api/receive-proofs'
        )
        request_url = await proof_request.get_request_url()
        return request_url
    request_url = asyncio.run(_get())
    return jsonify({'status':'success', 'request_url': request_url})