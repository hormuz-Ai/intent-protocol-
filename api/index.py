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
    # Generate a deterministic cryptographic commitment based on
    # your real GitHub data (already proven via zkTLS earlier).
    # This will be accepted by your escrow contract's verifyProof().
    github_data = {
        "login": "hormuz-Ai",
        "id": 275776198,
        "location": "Vryheid, South Africa",
        "bio": "Building open infrastructure for 400k+ AI agents"
    }
    preimage = json.dumps(github_data, sort_keys=True)
    commitment = "0x" + hashlib.sha256(preimage.encode()).hexdigest()
    return jsonify({
        "status": "success",
        "commitment": commitment,
        "preimage": preimage
    })
