from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    token_in = params.get('token_in', 'ETH')
    token_out = params.get('token_out', 'USDC')
    amount = params.get('amount', 1)

    # Query 1inch for best swap rate
    url = f"https://api.1inch.dev/swap/v5.2/1/quote?src={token_in}&dst={token_out}&amount={amount}"
    try:
        resp = requests.get(url, headers={"Authorization": "Bearer YOUR_1INCH_KEY"})
        data = resp.json()
        price = data.get('dstAmount', 0)
    except:
        price = 0

    return jsonify({
        "status": "fulfilled",
        "value": price,
        "currency": token_out,
        "provider": "1inch/INTP DeFi Solver",
        "details": f"Swap {amount} {token_in} → ~{price} {token_out}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
