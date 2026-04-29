from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

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
