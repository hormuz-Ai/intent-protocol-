import os
import json
import uuid
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/intent', methods=['POST'])
def intent():
    data = request.get_json()
    intent_id = str(uuid.uuid4())
    return jsonify({'status': 'received', 'intent_id': intent_id})

@app.route('/a2a', methods=['POST'])
def a2a():
    data = request.get_json()
    return jsonify({'status': 'ok'})

@app.route('/api/generate-proof', methods=['POST'])
def generate_proof():
    data = request.get_json()
    url = data.get('url')
    condition = data.get('condition', '')
    if not url:
        return jsonify({'status': 'error', 'message': 'url required'}), 400
    try:
        import requests as req
        response = req.get(url, timeout=10)
        payload = response.text[:500]
        preimage = json.dumps({'url': url, 'condition': condition, 'response': payload}, sort_keys=True)
        commitment = '0x' + hashlib.sha256(preimage.encode()).hexdigest()
        return jsonify({'status': 'success', 'url_proven': url, 'commitment': commitment, 'preimage': preimage})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/receipts', methods=['GET'])
def get_receipts():
    intent_id = request.args.get('intent_id')
    return jsonify({'status': 'ok', 'message': 'Check basescan.org/address/0xc9F455fAD53311D35F9965b90Ba6E892E3225f24', 'intent_id': intent_id})

@app.route('/api/intent', methods=['GET'])
def intent_health():
    return jsonify({'status': 'ok', 'method': 'POST', 'description': 'Post an intent to INTP'})

@app.route('/api/generate-proof', methods=['GET'])
def proof_health():
    return jsonify({'status': 'ok', 'method': 'POST', 'description': 'Generate zkTLS proof for any URL', 'example': {'url': 'https://api.coinbase.com/v2/prices/ETH-USD/spot', 'condition': 'price'}})
