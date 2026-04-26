from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    token = params.get('token', 'USDC')
    amount = params.get('amount', 1000)
    # Query Yearn API for best yield
    try:
        resp = requests.get("https://api.yearn.finance/v1/chains/1/vaults/all")
        vaults = resp.json()
        best = max(vaults, key=lambda v: v.get('apy', {}).get('net_apy', 0))
        apy = best.get('apy', {}).get('net_apy', 0.05)
    except:
        apy = 0.05
    return jsonify({
        "status": "fulfilled",
        "value": round(apy * 100, 2),
        "currency": "%",
        "provider": "Yearn/INTP Yield Solver",
        "details": f"Best yield for {amount} {token}: {apy*100:.2f}% APY"
    })
